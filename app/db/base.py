# filepath: app/db/base.py
from sqlmodel import create_engine, Session, SQLModel
from app.core.config import settings

connect_args = {"check_same_thread": False}
engine = create_engine(settings.DATABASE_URL, connect_args=connect_args)

def get_session():
    with Session(engine) as session:
        yield session



def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

