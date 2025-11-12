# محل تنظیمات کلی پروژه

import os
from pydantic import BaseModel


class Settings(BaseModel):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./todo.db")
    APP_NAME: str = "Fleare Planner Todo API"
    PAGE_SIZE: int = 20


settings = Settings()
DATABASE_URL = settings.DATABASE_URL