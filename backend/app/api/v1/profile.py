"""Роутер профиля: GET/PATCH /api/v1/profile (раздел 49 ТЗ)."""

from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.game_utils import exp_to_next_level
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import ProfileResponse, ProfileUpdate, StatsBlock

router = APIRouter(prefix="/profile", tags=["profile"])


def _serialize_profile(user: User) -> ProfileResponse:
    """Собирает ответ профиля из User + Profile."""
    return ProfileResponse(
        id=user.id,
        username=user.username,
        display_name=user.profile.display_name if user.profile else None,
        level=user.level,
        experience=user.experience,
        exp_to_next=exp_to_next_level(user.level),
        stats=StatsBlock(
            strength=user.strength,
            endurance=user.endurance,
            core=user.core,
            recovery=user.recovery,
        ),
        created_at=user.created_at,
    )


@router.get("", response_model=ProfileResponse)
def get_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ProfileResponse:
    """Возвращает профиль и игровые характеристики текущего пользователя."""
    return _serialize_profile(current_user)


@router.patch("", response_model=ProfileResponse)
def update_profile(
    body: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ProfileResponse:
    """Обновляет редактируемые поля профиля."""
    if current_user.profile is None:
        from app.models.user import Profile

        current_user.profile = Profile(user_id=current_user.id)
        db.add(current_user.profile)

    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_user.profile, field, value)

    db.commit()
    db.refresh(current_user)
    return _serialize_profile(current_user)
