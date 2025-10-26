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


class TaskTags(str, Enum):
    administrative = 'administrative'
    normal = 'normal'


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[TaskStatus] = TaskStatus.todo
    priority: Optional[int] = 3
    tags: Optional[TaskTags] = TaskTags.normal
    Time_required: Optional[int] = 60
    is_complete:Optional[bool] = False 
    due_date:Optional[datetime]=datetime.now()


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    id: Optional[int] = None
    title: Optional[str]
    description: Optional[str]
    status: Optional[TaskStatus] = TaskStatus.todo
    priority: Optional[int]
    tags: Optional[TaskTags] = TaskTags.normal
    Time_required: Optional[int] = 60
    is_complete:Optional[bool]


class TaskResponse(TaskBase):
    id: int
    title: str
    description: Optional[str] = None
    priority: int
    status: Optional[str] = None
    Time_required: Optional[int] = 60
    due_date: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    tags: Optional[TaskTags] = TaskTags.normal
    owner_id: Optional[int] = None
    is_deleted: bool
    is_complete:bool

    class Config:
        from_attributes = True
