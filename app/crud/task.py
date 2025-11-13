# عملیات CRUD برای مدل Task
from http.client import HTTPException
from datetime import datetime, timedelta
from app.models.task import Task
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, time, date,timezone
from app.schemas.task import TaskCreate, TaskUpdate
from sqlalchemy import or_


def get_tasks(db: Session):

    now = datetime.now()
    # tasks = db.query(Task).filter(Task.is_deleted == False).filter(Task.is_complete==False).all()
    tasks = db.query(Task).filter(Task.status.in_(['todo','missed'])).filter(Task.is_deleted == False).all()
    in_progress_tasks = db.query(Task).filter(Task.status == 'in_progress').filter(Task.is_deleted == False).all()
    done_tasks=db.query(Task).filter(Task.status == "done").filter(Task.is_deleted == False).all()

    # تسک‌های اداری جلوتر از نرمال
    def tag_priority(tags):
        if "administrative" in tags:
            return 0
        else:
            return 1
    tasks.sort(key=lambda t: (tag_priority(t.tags), t.priority, 3 if t.status == "missed" else 2, t.due_date))
    in_progress_tasks.sort(key=lambda t: t.due_date)
    done_tasks.sort(key=lambda t : t.due_date)
    for t in done_tasks:
        db.expunge(t)
    organized_tasks=[]
    static_end_times=[
        t.due_date + timedelta(minutes=getattr(t,"Time_required",60))
        for t in in_progress_tasks if t.due_date is not None 
    ]
    for i in in_progress_tasks:
        print(i.due_date)
    last_static_end=max(static_end_times)if static_end_times else now

    ADMIN_START, ADMIN_END = time(8, 0), time(14, 0)
    NORMAL_START, NORMAL_END = time(8, 0), time(22, 0)
    day_usage = {}
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
            if start_time <last_static_end:
                start_time=last_static_end
            
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
        last_static_end=end_time
        
        
        organized_tasks.append(task)
    last_organized=[]
    last_organized.extend(done_tasks)
    last_organized.extend(in_progress_tasks)
    last_organized.extend(organized_tasks)
    return last_organized

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
    return True
