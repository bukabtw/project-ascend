"""Роутер упражнений: GET/POST /api/v1/exercises (разделы 26, 49 ТЗ)."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.exercise import Exercise
from app.models.user import User
from app.schemas.exercise import ExerciseCreate, ExerciseResponse

router = APIRouter(prefix="/exercises", tags=["exercises"])


@router.get("", response_model=list[ExerciseResponse])
def list_exercises(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[Exercise]:
    """Возвращает все упражнения (встроенные и пользовательские)."""
    stmt = select(Exercise).order_by(Exercise.name)
    return list(db.scalars(stmt))


@router.post(
    "",
    response_model=ExerciseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_exercise(
    body: ExerciseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Exercise:
    """Создаёт пользовательское упражнение."""
    existing = db.scalar(select(Exercise).where(Exercise.name == body.name))
    if existing is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Exercise with this name already exists",
        )

    exercise = Exercise(
        name=body.name,
        category=body.category,
        measurement_type=body.measurement_type,
        unit=body.unit,
        description=body.description,
        is_custom=True,
        created_by=current_user.id,
    )
    db.add(exercise)
    db.commit()
    db.refresh(exercise)
    return exercise
