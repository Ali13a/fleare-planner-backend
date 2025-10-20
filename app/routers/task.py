# تعریف endpointهای مربوط به task

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from starlette import schemas

from app.crud import task
from app.deps import get_db
from app.models.task import Task
from app.schemas.task import TaskResponse, TaskCreate

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/")
def get_tasks(db: Session = Depends(get_db)):
    tasks = task.get_tasks(db)
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found")
    return {"results": tasks}

@router.get("/{task_title}")
def get_task_by_title(task_title: str, db: Session = Depends(get_db)):
    task_obj = task.get_task_by_title(db, task_title)
    if not task_obj:
        raise HTTPException(status_code=404, detail="No tasks found")
    return task_obj


@router.post("/create", response_model=TaskResponse, status_code=201)
def create_new_task(t: TaskCreate, db: Session = Depends(get_db)):
    created_task = task.create_task(db, t)
    if not created_task:
        raise HTTPException(status_code=400, detail="Task not created")
    return created_task
