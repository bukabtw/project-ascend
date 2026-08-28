"""Модели упражнений и калибровки (разделы 24-26 ТЗ)."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin
from app.models.enums import ExerciseCategory, MeasurementType, enum_values


class Exercise(Base, TimestampMixin):
    """Упражнение (встроенное или пользовательское) — раздел 26 ТЗ."""

    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), unique=True, index=True, nullable=False)
    category: Mapped[ExerciseCategory] = mapped_column(
        Enum(ExerciseCategory, values_callable=enum_values), nullable=False
    )
    measurement_type: Mapped[MeasurementType] = mapped_column(
        Enum(MeasurementType, values_callable=enum_values), nullable=False
    )
    unit: Mapped[str] = mapped_column(String(32), nullable=False)
    description: Mapped[str | None] = mapped_column(String(512), nullable=True)
    is_custom: Mapped[bool] = mapped_column(default=False, nullable=False)
    created_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    calibration_records: Mapped[list[CalibrationRecord]] = relationship(
        back_populates="exercise"
    )


class CalibrationRecord(Base):
    """Результат калибровочного теста пользователя (раздел 25 ТЗ).

    Хранится отдельной таблицей, а не JSON-полем внутри ``users``.
    """

    __tablename__ = "calibration_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    exercise_id: Mapped[int] = mapped_column(
        ForeignKey("exercises.id", ondelete="CASCADE"), index=True, nullable=False
    )
    value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String(32), nullable=False)
    performed_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    notes: Mapped[str | None] = mapped_column(String(512), nullable=True)

    exercise: Mapped[Exercise] = relationship(back_populates="calibration_records")
