from fastapi import FastAPI
from app.routers.task import router
from app.db.base import Base
from app.db.session import engine
from fastapi.middleware.cors import CORSMiddleware


def create_app():
    mainApp = FastAPI(title="Flare Planner Todo API")

    mainApp.include_router(router)

    mainApp.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:4200"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return mainApp


app = create_app()

Base.metadata.create_all(bind=engine)