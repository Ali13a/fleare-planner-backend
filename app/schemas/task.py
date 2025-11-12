# app/schemas/task.py
from datetime import datetime
from pydantic import BaseModel,Field
from typing import Optional
from enum import Enum


class TaskStatus(str, Enum):
    todo = "todo"
    in_progress = "in_progress"
    done = "done"
    archived = "archived"
    missed='missed'


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
    is_complete: Optional[bool] = False
    due_date: Optional[datetime] =None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[int] = None
    tags: Optional[TaskTags] = None
    Time_required: Optional[int] = None
    is_complete: Optional[bool] = None
    due_date:Optional[datetime]=None
    end_time:Optional[datetime]=None

    class Config:
        extra = "ignore"


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
    is_complete: Optional[bool] = False
    is_deleted: bool
    end_time:Optional[datetime]=None

    class Config:
        from_attributes = True
