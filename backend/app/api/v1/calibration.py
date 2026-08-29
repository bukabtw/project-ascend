"""Роутер калибровки: POST/GET /api/v1/calibration (разделы 24-25, 49 ТЗ)."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.exercise import CalibrationRecord, Exercise
from app.models.user import User
from app.schemas.exercise import CalibrationCreate, CalibrationResponse

router = APIRouter(prefix="/calibration", tags=["calibration"])


@router.post("", response_model=CalibrationResponse, status_code=status.HTTP_201_CREATED)
def create_calibration(
    body: CalibrationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> CalibrationResponse:
    """Сохраняет результат калибровочного теста."""
    exercise = db.get(Exercise, body.exercise_id)
    if exercise is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise not found",
        )

    record = CalibrationRecord(
        user_id=current_user.id,
        exercise_id=body.exercise_id,
        value=body.value,
        unit=body.unit,
        performed_at=body.performed_at,
        notes=body.notes,
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return CalibrationResponse(
        id=record.id,
        exercise_id=record.exercise_id,
        exercise_name=exercise.name,
        value=record.value,
        unit=record.unit,
        performed_at=record.performed_at,
        notes=record.notes,
    )


@router.get("", response_model=list[CalibrationResponse])
def list_calibrations(
    exercise_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> list[CalibrationResponse]:
    """Возвращает историю калибровочных записей пользователя."""
    stmt = (
        select(CalibrationRecord, Exercise.name)
        .join(Exercise, CalibrationRecord.exercise_id == Exercise.id)
        .where(CalibrationRecord.user_id == current_user.id)
        .order_by(CalibrationRecord.performed_at.desc())
    )
    if exercise_id is not None:
        stmt = stmt.where(CalibrationRecord.exercise_id == exercise_id)

    rows = db.execute(stmt).all()
    return [
        CalibrationResponse(
            id=record.id,
            exercise_id=record.exercise_id,
            exercise_name=exercise_name,
            value=record.value,
            unit=record.unit,
            performed_at=record.performed_at,
            notes=record.notes,
        )
        for record, exercise_name in rows
    ]
