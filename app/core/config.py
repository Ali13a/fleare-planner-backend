# محل تنظیمات کلی پروژه

import os
from pathlib import Path
from pydantic import BaseModel

BASE_DIR=Path(__file__).resolve().parent.parent
DB_PATH=BASE_DIR / "todo.db"

class Settings(BaseModel):
    DATABASE_URL: str =f"sqlite:///{DB_PATH}"
    APP_NAME: str = "Fleare Planner Todo API"
    PAGE_SIZE: int = 20



settings = Settings()
DATABASE_URL = settings.DATABASE_URL
print("Database path:",DATABASE_URL)
print("database absoulute path:",DB_PATH)
