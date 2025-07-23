from pydantic import BaseModel
from app.db.models import User

class Token(BaseModel):
    access_token: str
    token_type: str
