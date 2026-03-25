from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.db.models import User
from app.db.schemas.auth import AuthResponse, CurrentUserResponse, LoginRequest, SignupRequest
from app.services.auth_service import get_current_user_response, login_user, signup_user

router = APIRouter()


@router.post("/signup", response_model=AuthResponse)
def signup(payload: SignupRequest, db: Session = Depends(get_db)) -> AuthResponse:
    return signup_user(db, payload)


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> AuthResponse:
    return login_user(db, payload)


@router.get("/me", response_model=CurrentUserResponse)
def me(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CurrentUserResponse:
    return get_current_user_response(db, current_user)
