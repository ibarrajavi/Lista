from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings
from pathlib import Path

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

