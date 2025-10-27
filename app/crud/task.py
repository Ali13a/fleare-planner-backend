# عملیات CRUD برای مدل Task
from http.client import HTTPException
from datetime import datetime, timedelta
from app.models.task import Task
from sqlalchemy.orm import Session
from sqlalchemy import Case
from datetime import datetime, timedelta, time, date
from app.schemas.task import TaskCreate, TaskUpdate
from sqlalchemy.sql import func


def get_tasks(db: Session):
    now = datetime.now()
    now2= date.today()
    tasks = db.query(Task).filter(func.date(Task.due_date)==now2).filter(Task.is_deleted == False).filter(Task.is_complete==False).all()
    # tasks = db.query(Task).filter(func.date(Task.due_date)==now2).filter(Task.is_deleted == False).all();

    # تسک‌های اداری جلوتر از نرمال
    def tag_priority(tags):
        if "administrative" in tags:
            return 0
        else:
            return 1
    tasks.sort(key=lambda t: (3 if t.due_date < now else 2, tag_priority(t.tags) , t.created_at))

    organized_tasks = []
    pastdate=[]

    ADMIN_START, ADMIN_END = time(8, 0), time(14, 0)
    NORMAL_START, NORMAL_END = time(8, 0), time(22, 0)

    day_usage = {}  # {date: {"last_task": datetime}}

    for task in tasks:
        duration = getattr(task, "Time_required", 60)
        is_admin = "administrative" in (task.tags or [])
        task_day = max(task.due_date.date() if task.due_date else now.date(), now.date())

        # اگر از بازه امروز گذشته، بنداز روز بعد
        if is_admin and now.time() >= ADMIN_END:
            task_day += timedelta(days=1)
        elif not is_admin and now.time() >= NORMAL_END:
            task_day += timedelta(days=1)

        # آماده‌سازی روز
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

        #if task.due_date.date() == now.date():
            #organized_tasks.append(task)

        organized_tasks.append(task)

    

    return organized_tasks


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


def update_task(db: Session, id: int, t: TaskUpdate):
    task = db.query(Task).filter(Task.id == id, Task.is_deleted == False).first()

    if not task:
        return None

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
