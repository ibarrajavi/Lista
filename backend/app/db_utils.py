from sqlalchemy.orm import Session
from typing import Any

class DatabaseUtils:
    def __init__(self, db: Session) -> None:
        self.db = db

    def db_get(
            self,
            model,
            record_id: int,
            model_name: str = "Record"
    ) -> Any:
        """
        Retrieve a record by its primary key.
        """
        try:
            res = self.db.get(model, record_id)
        except Exception as e:
            raise RuntimeError(f"{model_name} database error: {str(e)}")
        
        if res is None:
            raise ValueError(f"{model_name} not found")
        
        return res
    
    def db_commit(self) -> None:
        """
        Commit the current transaction.
        """
        try:
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise RuntimeError(f"Commit failed: {str(e)}")
        
    def db_create(self, instance) -> Any:
        """
        Add and commit the current transaction.
        """
        try:
            self.db.add(instance)
            self.db.commit()
            self.db.refresh(instance)
        except Exception as e:
            self.db.rollback()
            raise RuntimeError(f"Creation failed: {str(e)}")
        
    def db_delete(self, instance) -> None:
        """
        Delete and commit a record.
        """
        try:
            self.db.delete(instance)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise RuntimeError(f"Deletion failed: {str(e)}")

