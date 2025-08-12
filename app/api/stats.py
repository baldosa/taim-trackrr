from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from datetime import timedelta
from app.db.base import get_session
from app.core.data import get_all_timespan
from app.db.models import TimeSpan, User
from app.core.security import get_current_user

router = APIRouter()

SessionDep = Annotated[Session, Depends(get_session)]

@router.get("/data")
async def get_raw_data(
    current_user: Annotated[User, Depends(get_current_user)],
    session: SessionDep
) -> list[TimeSpan]:
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    else:
        timespan = get_all_timespan(session, user_id=current_user.id)
        if not timespan:
            raise HTTPException(status_code=404, detail="No active timer found")
        return timespan

@router.get("/summary")
async def get_stats(
    current_user: Annotated[User, Depends(get_current_user)],
    session: SessionDep
):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    else:
        timespan = get_all_timespan(session, user_id=current_user.id)
        if not timespan:
            raise HTTPException(status_code=404, detail="No active timer found")

        return {
            "total_time": sum([ts.end_time - ts.start_time for ts in timespan], timedelta()),
            "average_time": (sum([ts.end_time - ts.start_time for ts in timespan], timedelta()) / len(timespan)) if timespan else 0,
            "timespan_count": len(timespan) 
        }