"""Роутер пользователей: регистрация (раздел 49 ТЗ)."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.db.session import get_db
from app.models.user import Profile, User
from app.schemas.user import UserCreateResponse, UserRegister

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", response_model=UserCreateResponse, status_code=status.HTTP_201_CREATED)
def register(body: UserRegister, db: Session = Depends(get_db)) -> User:
    """Регистрация нового пользователя.

    Создаёт запись в ``users`` с bcrypt-хэшем пароля и пустой профиль.
    """
    existing = db.scalar(select(User).where(User.username == body.username))
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already taken",
        )

    user = User(
        username=body.username,
        password_hash=hash_password(body.password),
    )
    user.profile = Profile()
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
