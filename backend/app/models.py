from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship
from datetime import datetime, timezone
from app.database import Base

class List(Base):
    __tablename__ = "list"

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    tasks = relationship("Task", back_populates="list", cascade="all, delete-orphan")

class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True)
    list_id = Column(Integer, ForeignKey("list.id"), index=True, nullable=False)
    description = Column(String(256), nullable=False)
    position = Column(Integer, nullable=False)
    is_complete = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    list = relationship("List", back_populates="tasks")

