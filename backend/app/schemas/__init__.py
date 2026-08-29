"""Pydantic-схемы Ascend (request/response модели API)."""

from app.schemas.exercise import (
    CalibrationCreate,
    CalibrationResponse,
    ExerciseCreate,
    ExerciseResponse,
)
from app.schemas.user import (
    ProfileResponse,
    ProfileUpdate,
    StatsBlock,
    UserCreateResponse,
    UserRegister,
)

__all__ = [
    "CalibrationCreate",
    "CalibrationResponse",
    "ExerciseCreate",
    "ExerciseResponse",
    "ProfileResponse",
    "ProfileUpdate",
    "StatsBlock",
    "UserCreateResponse",
    "UserRegister",
]
