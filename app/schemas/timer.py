from pydantic import BaseModel
from app.db.models import TimeSpan

class TimerResponse(BaseModel):
    timespan: TimeSpan
    created: bool