# تعریف endpointهای مربوط به task

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.crud import task
from app.deps import get_db
from app.schemas.task import TaskResponse, TaskCreate, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/")
def get_tasks(db: Session = Depends(get_db)):
    tasks = task.get_tasks(db)
    # if not tasks:
    #     raise HTTPException(status_code=404, detail="No tasks found")
    return tasks


@router.get("/{task_id}")
def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
    tasks = task.get_task_by_id(db, task_id)
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found")
    return tasks


@router.get("/title/{task_title}")
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


@router.put("/update/{id}", response_model=TaskResponse, status_code=200)
def update_task(id: int, t: TaskUpdate, db: Session = Depends(get_db)):
    updated_task = task.update_task(db, id, t)

    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")

    return updated_task


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    deleted_task = task.delete_task(db, task_id)
    if not deleted_task:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task deleted successfully"}
