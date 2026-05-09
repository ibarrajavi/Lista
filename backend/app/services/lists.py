# --- Third-party
from sqlalchemy import select
from sqlalchemy.orm import Session

# --- Standard library
from uuid import UUID

# --- Local application
from app.models.models import List
from app.core.db_utils import DatabaseUtils
from app.core.exceptions import ListNotFoundError


def get_list(db: Session, list_id: UUID, user_id: UUID) -> List:
    existing_list = db.get(List, list_id)
    if existing_list is None or existing_list.user_id != user_id:
        raise ListNotFoundError()
    return existing_list


def create_list(db: Session, name: str, user_id: UUID) -> List:
    db_utils = DatabaseUtils(db)
    new_list = List(name=name.strip(), user_id=user_id)
    return db_utils.db_create(new_list)


def rename_list(db: Session, list_id: UUID, name: str, user_id: UUID) -> List:
    db_utils = DatabaseUtils(db)
    existing_list = get_list(db, list_id, user_id)
    existing_list.name = name.strip()
    db_utils.db_commit()
    return existing_list


def get_lists(db: Session, user_id: UUID) -> list[List]:
    res = db.execute(select(List).where(List.user_id == user_id))
    return res.scalars().all()


def delete_list(db: Session, list_id: UUID, user_id: UUID) -> None:
    db_utils = DatabaseUtils(db)
    existing_list = get_list(db, list_id, user_id)
    db_utils.db_delete(existing_list)
