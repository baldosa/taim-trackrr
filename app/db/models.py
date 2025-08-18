from sqlmodel import SQLModel, Field
from datetime import datetime

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class TimeSpan(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    start_time: datetime = Field(default_factory=lambda: datetime.now())
    end_time: datetime  | None = None
    user_id: int = Field(foreign_key="user.id")
    note: str | None = None
    tags: str | None = None
