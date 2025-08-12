from datetime import datetime
from sqlmodel import Session, select
from app.db.models import TimeSpan


def get_all_timespan(session: Session, user_id: int) -> list[TimeSpan]:
    """Get all timespans for the user."""
    statement = select(TimeSpan).where(
        TimeSpan.user_id == user_id,
        TimeSpan.end_time != None
    ).order_by(TimeSpan.start_time.desc())
    return session.exec(statement).all()
