# --- Third-party
from sqlalchemy import select, update, func
from sqlalchemy.orm import Session

# --- Local application
from app.models import Task
from app.db_utils import DatabaseUtils

def _next_position(db: Session, list_id: int) -> int:
    """
    Determine the next task position for a to-do list.
    """
    res = db.execute(
        select(func.max(Task.position)).where(Task.list_id == list_id)
    ).scalar()

    if res is None:
        return 1
    return res + 1

def _reindex_positions(
        db: Session, 
        list_id: int,
        old_position: int,
        new_position: int,
) -> None:
    """
    Shifts task positions within a list when a task is moved.
    """
    if new_position < old_position:
        # Moving up - shift tasks between new and old position down by 1
        db.execute(
            update(Task)
            .where(Task.list_id == list_id)
            .where(Task.position >= new_position)
            .where(Task.position < old_position)
            .values(position=Task.position + 1)
        )
    elif new_position > old_position:
        # Moving down - shift tasks between old and new position up by 1
        db.execute(
            update(Task)
            .where(Task.list_id == list_id)
            .where(Task.position > old_position)
            .where(Task.position <= new_position)
            .values(position=Task.position - 1)
        )

def _close_gap(db: Session, list_id: int, deleted_position: int) -> None:
    """
    Shifts task positions above the deleted task down by 1.
    """
    db.execute(
        update(Task)
        .where(Task.list_id == list_id)
        .where(Task.position > deleted_position)
        .values(position=Task.position - 1)
    )

def create_task(db: Session, list_id: int, description: str) -> Task:
    """
    Create a task for a to-do list.
    """
    db_utils = DatabaseUtils(db)

    position = _next_position(db, list_id)
    new_task = Task(
        list_id=list_id,
        description=description.strip(),
        position=position,
    )
    return db_utils.db_create(new_task)

def update_task(
        db: Session,
        task_id: int,
        *,
        description: str | None = None,
        position: int | None = None,
        is_complete: bool | None = None,
) -> Task:
    """
    Update a task description, position, or complete status.
    """
    db_utils = DatabaseUtils(db)
    existing_task = db_utils.db_get(Task, task_id, "Task")
    
    if description is not None:
        existing_task.description = description.strip()

    if position is not None and position >= 1:
        _reindex_positions(
            db,
            existing_task.list_id,
            existing_task.position,
            position
        )
        existing_task.position = position
    
    if is_complete is not None:
        existing_task.is_complete = is_complete

    db_utils.db_commit()
    return existing_task

def get_tasks(db: Session, list_id: int) -> list[Task]:
    """
    Retrieves all tasks in the specified to-do list.
    """
    res = db.execute(select(Task).where(Task.list_id == list_id).order_by(Task.position))
    return res.scalars().all()

def delete_task(db: Session, task_id: int) -> None:
    """
    Deletes an existing task in a to-do list and closes the position gap.
    """
    db_utils = DatabaseUtils(db)
    existing_task = db_utils.db_get(Task, task_id, "Task")
    _close_gap(db, existing_task.list_id, existing_task.position)
    db_utils.db_delete(existing_task)

