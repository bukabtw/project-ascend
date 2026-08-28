"""Модель готовности к нагрузке (разделы 16-19 ТЗ).

Вычисляемые показатели хранятся отдельно от сырых метрик.
"""

from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class ReadinessScore(Base):
    """Оценка готовности пользователя на конкретную дату (раздел 19 ТЗ)."""

    __tablename__ = "readiness_scores"
    __table_args__ = (
        # Одна оценка на пользователя в день.
        UniqueConstraint("user_id", "date", name="uq_readiness_user_date"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    date: Mapped[date] = mapped_column(Date, nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)  # 0-100
    training_modifier: Mapped[float] = mapped_column(Float, nullable=False)
    reason: Mapped[str | None] = mapped_column(String(256), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
