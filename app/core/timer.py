from datetime import datetime
from sqlmodel import Session, select
from app.db.models import TimeSpan

class TimerService:
    def __init__(self, session: Session):
        self.session = session

    def get_active_timespan(self, user_id: int) -> TimeSpan | None:
        """Get the most recent timespan with no end_time for the user."""
        statement = select(TimeSpan).where(
            TimeSpan.user_id == user_id,
            TimeSpan.end_time == None
        ).order_by(TimeSpan.start_time.desc())
        return self.session.exec(statement).first()

    def create_timespan(self, user_id: int, note: str = "", tags: str = "") -> TimeSpan:
        timespan = TimeSpan(
            start_time=datetime.now(),
            user_id=user_id,
            note=note,
            tags=tags
        )
        self.session.add(timespan)
        self.session.commit()
        self.session.refresh(timespan)
        return timespan

    def get_or_create_active_timespan(self, user_id: int, note: str = "", tags: str = "") -> tuple[TimeSpan, bool]:
        active_timespan = self.get_active_timespan(user_id)
        if active_timespan:
            return active_timespan, False
        return self.create_timespan(user_id, note, tags), True

    def end_active_timespan(self, user_id: int) -> TimeSpan | None:
        """End the active timespan by setting its end_time. Returns the updated timespan."""
        timespan = self.get_active_timespan(user_id)
        if not timespan:
            return None
        timespan.end_time = datetime.now()
        self.session.add(timespan)
        self.session.commit()
        self.session.refresh(timespan)
        return timespan