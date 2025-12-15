# عملیات CRUD برای مدل Task
from http.client import HTTPException
from datetime import datetime, timedelta
from app.models.task import Task
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, time, date
from app.schemas.task import TaskCreate, TaskUpdate


def get_tasks(db: Session):
    now = datetime.now()
    # tasks = db.query(Task).filter(Task.is_deleted == False).filter(Task.is_complete==False).all()
    tasks = db.query(Task).filter(Task.is_deleted == False).all()

    tasks.sort(key=lambda t: (t.is_overdue, "administrative" in t.tags, t.priority))

    organized_tasks = []

    ADMIN_START, ADMIN_END = time(8, 0), time(14, 0)
    NORMAL_START, NORMAL_END = time(8, 0), time(22, 0)

    day_usage = {}

    for task in tasks:
        duration = getattr(task, "Time_required", 60)
        is_admin = "administrative" in (task.tags or [])
        task_day = max(task.due_date.date() if task.due_date else now.date(), now.date())

        if is_admin and now.time() >= ADMIN_END:
            task_day += timedelta(days=1)
        elif not is_admin and now.time() >= NORMAL_END:
            task_day += timedelta(days=1)

        if task_day not in day_usage:
            day_usage[task_day] = {
                "last_task": datetime.combine(task_day, NORMAL_START)
            }

        while True:
            if is_admin:
                day_start = datetime.combine(task_day, ADMIN_START)
                day_end = datetime.combine(task_day, ADMIN_END)
            else:
                day_start = datetime.combine(task_day, NORMAL_START)
                day_end = datetime.combine(task_day, NORMAL_END)

            start_time = max(day_usage[task_day]["last_task"], day_start, now)
            end_time = start_time + timedelta(minutes=duration)

            if end_time <= day_end and start_time >= now:
                task.due_date = start_time
                day_usage[task_day]["last_task"] = end_time
                break
            else:
                task_day += timedelta(days=1)
                if task_day not in day_usage:
                    day_usage[task_day] = {
                        "last_task": datetime.combine(task_day, NORMAL_START)
                    }

        task.due_date = start_time

        organized_tasks.append(task)

    return organized_tasks


def get_task_by_id(db: Session, task_id: str):
    tasks = db.query(Task) \
        .filter(Task.id == task_id, Task.is_deleted == False) \
        .first()
    return tasks


def get_task_by_title(db: Session, task_title: str):
    tasks = (
        db.query(Task)
        .filter(Task.title.ilike(f"%{task_title}%"))
        .filter(Task.is_deleted == False)
        .all()
    )

    return tasks


def create_task(db: Session, t: TaskCreate):
    new_task = Task(**t.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def update_task(db: Session, id: int, t: TaskUpdate):
    task = db.query(Task).filter(Task.id == id, Task.is_deleted == False).first()
    if not task:
        return None

    update_data = t.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int):
    task = db.query(Task).filter(Task.id == task_id, Task.is_deleted == False).first()
    db.delete(task)
    db.commit()
    db.refresh()
    return True
