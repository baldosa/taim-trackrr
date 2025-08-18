from pydantic import BaseModel
from app.db.models import User

class Token(BaseModel):
    access_token: str
    token_type: str

class UserCreate(BaseModel):
    username: str
    password: str
    email: str | None = None
    full_name: str | None = None
