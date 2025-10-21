from fastapi import FastAPI
from app.routers.task import *
from app.db.base import Base
from app.db.session import engine

def create_app():
    mainApp = FastAPI(title="Fleare Planner Todo API")
    mainApp.include_router(router)
    return mainApp

app = create_app()

Base.metadata.create_all(bind=engine)
