from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.core.config import settings
from app.core.security import create_access_token, authenticate_user, get_current_user, create_new_user
from app.db.base import get_session
from app.db.models import User
from app.schemas.auth import Token, UserCreate

router = APIRouter()

SessionDep = Annotated[Session, Depends(get_session)]



@router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: SessionDep = get_session(), 

) -> Token:
    user = authenticate_user(session, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user



@router.post("/register", response_model=User)
async def register_user(
    current_user: Annotated[User, Depends(get_current_user)],
    user: UserCreate,
    session: Session = Depends(get_session)
) -> User:
    """
    Register a new user.
    """
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return create_new_user(session, user)