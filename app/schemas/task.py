# app/schemas/task.py
from datetime import datetime

from pydantic import BaseModel
from typing import Optional
from enum import Enum


class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"
    archived = "archived"
class TaskTags(str,Enum):
    administrative='administrative'
    normal='normal'


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[TaskStatus] = TaskStatus.todo
    priority: Optional[int] = 3
    tags: Optional[str] = TaskTags.normal
    Time_required:Optional[int]=60
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    id: Optional[int] = None
    title: Optional[str]
    description: Optional[str]
    status: Optional[TaskStatus] = TaskStatus.todo
    priority: Optional[int]
    tags: Optional[str]
    due_date: Optional[datetime]


class TaskResponse(TaskBase):
    id: int
    title: str
    description: Optional[str] = None
    priority: int
    status: Optional[str] = None
    due_date: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    tags: Optional[str] = None
    owner_id: Optional[int] = None
    is_deleted: bool

    class Config:
        from_attributes = True
