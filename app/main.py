from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.api import auth, timer
app = FastAPI(title="Taim Trackrr")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(timer.router, prefix="/api")