# عملیات CRUD برای مدل Task
from app.models.task import Task
from sqlalchemy.orm import Session

from app.schemas.task import TaskCreate


def get_tasks(db: Session):
    tasks = db.query(Task).all()
    return tasks


def get_task_by_title(db: Session, task_title: str):
    tasks = db.query(Task) \
        .filter(Task.title.ilike(f"%{task_title}%")) \
        .all()
    return tasks


def create_task(db: Session, t: TaskCreate):
    new_task = Task(**t.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task
