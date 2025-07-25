from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.db.base import get_session
from app.core.timer import TimerService
from app.db.models import TimeSpan, User
from app.schemas.timer import TimerResponse
from app.core.security import get_current_user

router = APIRouter()

SessionDep = Annotated[Session, Depends(get_session)]


@router.post("/timer")
async def create_timer(
    current_user: Annotated[User, Depends(get_current_user)],
    note: str = "",
    tags: str = "",
    session: SessionDep = get_session(),
) -> TimerResponse:
    timer_service = TimerService(session)
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    else:
        timespan, created = timer_service.get_or_create_active_timespan(
            user_id=current_user.id,
            note=note,
            tags=tags,
        )
        return TimerResponse(timespan=timespan, created=created)


@router.get("/timer/active")
async def get_active_timer(
    current_user: Annotated[User, Depends(get_current_user)],
    session: SessionDep
) -> TimeSpan:
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    else:
        timer_service = TimerService(session)
        timespan = timer_service.get_active_timespan(user_id=current_user.id)
        if not timespan:
            raise HTTPException(status_code=404, detail="No active timer found")
        return timespan


@router.post("/timer/end")
async def end_timer(
    current_user: Annotated[User, Depends(get_current_user)],
    session: SessionDep
) -> TimeSpan:
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    else:
        timer_service = TimerService(session)
        timespan = timer_service.end_active_timespan(user_id=current_user.id)
        if not timespan:
            raise HTTPException(status_code=404, detail="No active timer found to end")
        return timespan