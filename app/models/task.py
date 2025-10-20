# تعریف مدل ORM

from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from app.db.base import Base
import enum

class TaskStatus(str, enum.Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"
    archived = "archived"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.todo, index=True)
    priority = Column(Integer, default=3)  # 1 high - 5 low
    due_date = Column(DateTime, nullable=True, index=True,)
    tags = Column(String(50))
    owner_id = Column(Integer, nullable=True, index=True)  # for future auth
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    is_deleted = Column(Boolean, default=False)
