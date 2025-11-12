# عملیات CRUD برای مدل Task
from http.client import HTTPException
from datetime import datetime, timedelta
from app.models.task import Task
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, time, date,timezone
from app.schemas.task import TaskCreate, TaskUpdate
from sqlalchemy import or_


def get_tasks(db: Session):
    # try:
    #     now = datetime.now()
    #     tasks =db.query(Task).all()
    #     for t in tasks:
    #         print("Raw Task:",t.id,t.due_date,t.end_time,t.status)
    #     # 📝 فقط تسک‌های قابل زمان‌بندی
    #     schedulable_tasks = db.query(Task).filter(
    #         Task.status.in_(['todo','missed']),
    #         Task.is_deleted == False
    #     ).all()

    #     # 📝 تسک‌های در حال انجام و انجام شده بدون تغییر
    #     static_tasks = db.query(Task).filter(
    #         Task.status.in_(['in_progress']),
    #         Task.is_deleted == False
    #     ).all()

    #     # اولویت بندی برای schedulable_tasks
    #     def tag_priority(tags):
    #         if "administrative" in (tags or ""):
    #             return 0
    #         return 1

    #     schedulable_tasks.sort(
    #         key=lambda t: (tag_priority(t.tags), t.priority, 3 if t.status == "missed" else 2, t.due_date)
    #     )
    #     # 🔧 زمان‌بندی فقط برای تسک‌های schedulable
    #     ADMIN_START, ADMIN_END = time(8, 0), time(14, 0)
    #     NORMAL_START, NORMAL_END = time(8, 0), time(22, 0)
    #     day_usage = {}

    #     for task in schedulable_tasks:
    #         duration = getattr(task, "Time_required", 60)
    #         is_admin = "administrative" in (task.tags or "")
    #         task_day = max((task.due_date.date() if task.due_date else now.date()), now.date())

    #         # اگر زمان الان خارج از محدوده کاریه، روز بعد رو انتخاب کن
    #         if is_admin and now.time() >= ADMIN_END:
    #             task_day += timedelta(days=1)
    #         elif not is_admin and now.time() >= NORMAL_END:
    #             task_day += timedelta(days=1)

    #         if task_day not in day_usage:
    #             day_usage[task_day] = {"last_task": datetime.combine(task_day, NORMAL_START)}

    #         # زمان‌بندی امن با کنترل بازه‌ها
    #         while True:
    #             day_start = datetime.combine(task_day, ADMIN_START if is_admin else NORMAL_START)
    #             day_end = datetime.combine(task_day, ADMIN_END if is_admin else NORMAL_END)

    #             if not task.due_date or task.due_date < now:
    #                 start_time = max(day_usage[task_day]["last_task"], day_start, now)
    #             else:
    #                 start_time = task.due_date

    #             end_time = start_time + timedelta(minutes=duration)

    #             # اطمینان از محدوده کاری
    #             if start_time < day_start:
    #                 start_time = day_start
    #                 end_time = start_time + timedelta(minutes=duration)

    #             if end_time > day_end:
    #                 task_day += timedelta(days=1)
    #                 if task_day not in day_usage:
    #                     day_usage[task_day] = {"last_task": datetime.combine(task_day, NORMAL_START)}
    #                 continue
    #             task.due_date=start_time
    #             task.end_time=end_time
    #             day_usage[task_day]["last_task"] = end_time
    #             break

    #     # ترکیب static_tasks و schedulable_tasks بدون دستکاری تاریخ static_tasks
    #     organized_tasks = static_tasks + schedulable_tasks

    #     return organized_tasks
    # except Exception as e :
    #     print("Error",str(e))
    #     return []



    now = datetime.now()
    # tasks = db.query(Task).filter(Task.is_deleted == False).filter(Task.is_complete==False).all()
    tasks = db.query(Task).filter(Task.is_deleted == False).all()

    # تسک‌های اداری جلوتر از نرمال
    def tag_priority(tags):
        if "administrative" in tags:
            return 0
        else:
            return 1
    tasks.sort(key=lambda t: (3 if t.due_date < now else 2, tag_priority(t.tags) , t.priority))

    organized_tasks = []

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

        if task.due_date.date() == now.date():
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
    print('created_task called with:',t.dict())
    new_task = Task(**t.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    print("Task created with ID:",new_task.id)
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
    db.delete(task)
    db.commit()
    db.refresh()
    return True
