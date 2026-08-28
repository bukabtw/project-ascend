"""Модели пользователей и профилей (разделы 51, 6 ТЗ)."""

from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class User(Base, TimestampMixin):
    """Пользователь системы и его игровые характеристики (раздел 51 ТЗ)."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(
        String(64), unique=True, index=True, nullable=False
    )
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    # Игровой прогресс
    level: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    experience: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Характеристики (раздел 27 ТЗ)
    strength: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    endurance: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    core: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    recovery: Mapped[int] = mapped_column(Integer, default=1, nullable=False)

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    profile: Mapped[Profile] = relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan"
    )


class Profile(Base, TimestampMixin):
    """Дополнительные персональные данные пользователя (1:1 к User).

    Хранится отдельно от игровых характеристик, чтобы ``users`` оставалась
    компактной таблицей профиля/аккаунта.
    """

    __tablename__ = "profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True, index=True, nullable=False
    )

    display_name: Mapped[str | None] = mapped_column(String(64), nullable=True)
    birth_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    height_cm: Mapped[float | None] = mapped_column(Float, nullable=True)
    goal_notes: Mapped[str | None] = mapped_column(String(512), nullable=True)

    user: Mapped[User] = relationship(back_populates="profile")
