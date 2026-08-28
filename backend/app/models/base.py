"""Базовый класс моделей SQLAlchemy."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Базовый класс для всех моделей Ascend."""


class TimestampMixin:
    """Примесь, добавляющая ``created_at`` для всех записей с авто-заполнением."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )
