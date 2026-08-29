"""Pydantic-схемы для Exercise и Calibration (разделы 24-26, 49 ТЗ)."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import ExerciseCategory, MeasurementType

# --------------------------------------------------------------------------- #
#  Exercise
# --------------------------------------------------------------------------- #

class ExerciseResponse(BaseModel):
    """Упражнение в ответе API."""

    id: int
    name: str
    category: ExerciseCategory
    measurement_type: MeasurementType
    unit: str
    description: str | None = None
    is_custom: bool
    created_by: int | None = None

    model_config = ConfigDict(from_attributes=True)


class ExerciseCreate(BaseModel):
    """Создание пользовательского упражнения (POST /exercises)."""

    name: str = Field(..., min_length=2, max_length=128)
    category: ExerciseCategory
    measurement_type: MeasurementType
    unit: str = Field(..., max_length=32)
    description: str | None = Field(default=None, max_length=512)


# --------------------------------------------------------------------------- #
#  Calibration
# --------------------------------------------------------------------------- #

class CalibrationCreate(BaseModel):
    """Создание калибровочной записи (POST /calibration)."""

    exercise_id: int
    value: float = Field(..., gt=0)
    unit: str = Field(..., max_length=32)
    performed_at: datetime
    notes: str | None = Field(default=None, max_length=512)


class CalibrationResponse(BaseModel):
    """Калибровочная запись в ответе API."""

    id: int
    exercise_id: int
    exercise_name: str
    value: float
    unit: str
    performed_at: datetime
    notes: str | None = None

    model_config = ConfigDict(from_attributes=True)
