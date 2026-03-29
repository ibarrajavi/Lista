# --- Third-party
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

# --- Standard library
from typing import Dict, Optional

# --- Local application
from app.config import settings

engine = create_engine(settings.DATABASE_URL)

# Session factory and Base for models
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# FastAPI dependency to provide a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_db_status() -> Dict[str, Optional[str]]:
    """
    Verify database connection by executing a SQL statement. 
    """
    db_error = None

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "OK"
    except Exception as e:
        db_status = "unreachable"
        db_error = str(e)

    return {
        "db": db_status,
        "error": db_error,
    }

