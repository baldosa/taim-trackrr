from fastapi import FastAPI
from sqlmodel import SQLModel

from app.api import auth, timer
app = FastAPI(title="Taim Trackrr")


# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(timer.router, prefix="/api")