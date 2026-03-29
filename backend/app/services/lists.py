# --- Third-party
from sqlalchemy import select
from sqlalchemy.orm import Session

# --- Local application
from app.models import List
from app.db_utils import DatabaseUtils

def create_list(db: Session, name: str) -> List:
    """
    Create a new to-do list.
    """
    db_utils = DatabaseUtils(db)
    new_list = List(name=name.strip())
    return db_utils.db_create(new_list)

def rename_list(db: Session, list_id: int, name: str) -> List:
    """
    Rename an existing to-do list.
    """
    db_utils = DatabaseUtils(db)
    existing_list = db_utils.db_get(List, list_id, "List")
    existing_list.name = name.strip()
    db_utils.db_commit()
    return existing_list

def get_lists(db: Session) -> list[List]:
    """
    Retrieves all to-do lists.
    """
    res = db.execute(select(List))
    return res.scalars().all()

def delete_list(db: Session, list_id: int) -> None:
    """
    Deletes an existing to-do list and any linked tasks via cascade.
    """
    db_utils = DatabaseUtils(db)
    existing_list = db_utils.db_get(List, list_id, "List")
    db_utils.db_delete(existing_list)

