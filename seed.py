import os
from dotenv import load_dotenv
from sqlmodel import Session
from app.core.security import pwd_context
from app.db.base import engine
from app.db.models import User

load_dotenv()

with Session(engine) as session:
    user_data =User(
        id=1,
        username=os.getenv("DEFAULT_USERNAME", "admin"),
        hashed_password=pwd_context.hash(os.getenv("DEFAULT_PASSWORD", "admin")),
        email=os.getenv("DEFAULT_EMAIL", "user@user.com"),
        full_name=os.getenv("DEFAULT_FULL_NAME", "user"),
        disabled=False,
    )
    session.add(user_data)
    session.commit()
    session.refresh(user_data)
    print(f"Superuser created: {user_data.username} with ID {user_data.id}")
    session.close()