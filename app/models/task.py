# تعریف مدل ORM
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base
from app.schemas.task import TaskStatus, TaskTags


def round_to_minute():
    now = datetime.utcnow()
    return now.replace(second=0, microsecond=0)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.todo, index=True)
    priority = Column(Integer, default=3)  # 1 high - 5 low
    Time_required = Column(Integer, nullable=True)
    due_date = Column(DateTime, nullable=True, index=True, )
    tags = Column(Enum(TaskTags), default=TaskTags.normal, index=True)
    owner_id = Column(Integer, nullable=True, index=True)  # for future auth
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    is_deleted = Column(Boolean, default=False)
    is_complete= Column(Boolean, default=False)
