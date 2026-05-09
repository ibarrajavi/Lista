# --- Third-party
from sqlalchemy import select, update, func
from sqlalchemy.orm import Session

# --- Standard library
from uuid import UUID

# --- Local application
from app.models.models import Task
from app.core.db_utils import DatabaseUtils
from app.core.exceptions import TaskNotFoundError


def _next_position(db: Session, list_id: UUID) -> int:
    res = db.execute(
        select(func.max(Task.position)).where(Task.list_id == list_id)
    ).scalar()
    return 1 if res is None else res + 1


def _reindex_positions(
        db: Session,
        list_id: UUID,
        old_position: int,
        new_position: int,
) -> None:
    if new_position < old_position:
        db.execute(
            update(Task)
            .where(Task.list_id == list_id)
            .where(Task.position >= new_position)
            .where(Task.position < old_position)
            .values(position=Task.position + 1)
        )
    elif new_position > old_position:
        db.execute(
            update(Task)
            .where(Task.list_id == list_id)
            .where(Task.position > old_position)
            .where(Task.position <= new_position)
            .values(position=Task.position - 1)
        )


def _close_gap(db: Session, list_id: UUID, deleted_position: int) -> None:
    db.execute(
        update(Task)
        .where(Task.list_id == list_id)
        .where(Task.position > deleted_position)
        .values(position=Task.position - 1)
    )


def create_task(db: Session, list_id: UUID, description: str) -> Task:
    db_utils = DatabaseUtils(db)
    position = _next_position(db, list_id)
    new_task = Task(list_id=list_id, description=description.strip(), position=position)
    return db_utils.db_create(new_task)


def update_task(
        db: Session,
        task_id: UUID,
        list_id: UUID,
        *,
        description: str | None = None,
        position: int | None = None,
        is_complete: bool | None = None,
) -> Task:
    db_utils = DatabaseUtils(db)
    existing_task = db.get(Task, task_id)
    if existing_task is None or existing_task.list_id != list_id:
        raise TaskNotFoundError()

    if description is not None:
        existing_task.description = description.strip()
    if position is not None and position >= 1:
        _reindex_positions(db, existing_task.list_id, existing_task.position, position)
        existing_task.position = position
    if is_complete is not None:
        existing_task.is_complete = is_complete

    db_utils.db_commit()
    return existing_task


def get_tasks(db: Session, list_id: UUID) -> list[Task]:
    res = db.execute(select(Task).where(Task.list_id == list_id).order_by(Task.position))
    return res.scalars().all()


def delete_task(db: Session, task_id: UUID, list_id: UUID) -> None:
    db_utils = DatabaseUtils(db)
    existing_task = db.get(Task, task_id)
    if existing_task is None or existing_task.list_id != list_id:
        raise TaskNotFoundError()
    _close_gap(db, existing_task.list_id, existing_task.position)
    db_utils.db_delete(existing_task)
