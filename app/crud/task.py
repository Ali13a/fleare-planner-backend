# عملیات CRUD برای مدل Task
from http.client import HTTPException

from app.models.task import Task
from sqlalchemy.orm import Session

from app.schemas.task import TaskCreate, TaskUpdate


def get_tasks(db: Session):
    tasks = db.query(Task).filter(Task.is_deleted == False).all()
    return tasks


def get_task_by_id(db: Session, task_id: str):
    tasks = db.query(Task) \
        .filter(Task.id == task_id, Task.is_deleted == False) \
        .first()
    return tasks


def get_task_by_title(db: Session, task_title: str):
    tasks = db.query(Task) \
        .filter(Task.title.ilike(f"%{task_title}%"), Task.is_deleted == False) \
        .all()
    return tasks


def create_task(db: Session, t: TaskCreate):
    new_task = Task(**t.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def update_task(db: Session, t: TaskUpdate):
    task = db.query(Task).filter(Task.id == t.id, Task.is_deleted == False).first()

    for key, value in t.dict(exclude_unset=True).items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id, Task.is_deleted == False).first()
    task.is_deleted = True
    db.commit()
    return True
