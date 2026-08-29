"""Pydantic-схемы для User и Profile (разделы 49, 51 ТЗ)."""

from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

# --------------------------------------------------------------------------- #
#  User
# --------------------------------------------------------------------------- #

class UserRegister(BaseModel):
    """Тело запроса регистрации нового пользователя."""

    username: str = Field(..., min_length=3, max_length=64)
    password: str = Field(..., min_length=6, max_length=128)


class UserCreateResponse(BaseModel):
    """Ответ после успешной регистрации."""

    id: int
    username: str
    level: int
    experience: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# --------------------------------------------------------------------------- #
#  Profile
# --------------------------------------------------------------------------- #

class StatsBlock(BaseModel):
    """Игровые характеристики пользователя."""

    strength: int
    endurance: int
    core: int
    recovery: int


class ProfileResponse(BaseModel):
    """Профиль пользователя с игровыми характеристиками (GET /profile)."""

    id: int
    username: str
    display_name: str | None = None
    level: int
    experience: int
    exp_to_next: int
    stats: StatsBlock
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProfileUpdate(BaseModel):
    """Обновляемые поля профиля (PATCH /profile)."""

    display_name: str | None = Field(default=None, max_length=64)
    birth_date: date | None = None
    height_cm: float | None = Field(default=None, gt=0, lt=300)
    goal_notes: str | None = Field(default=None, max_length=512)
