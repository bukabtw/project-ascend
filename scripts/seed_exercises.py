"""Сидинг начальных упражнений (раздел 24 ТЗ).

Запуск:
    python scripts/seed_exercises.py

Создаёт 5 базовых упражнений, если их ещё нет в БД:
отжимания, подтягивания, приседания, планка, бег.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Добавляем backend в sys.path, чтобы работали импорты app.*
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from app.db.session import SessionLocal
from app.models.enums import ExerciseCategory, MeasurementType
from app.models.exercise import Exercise

# (name, category, measurement_type, unit, description)
BUILTIN_EXERCISES: list[tuple[str, ExerciseCategory, MeasurementType, str, str]] = [
    ("Push-ups", ExerciseCategory.STRENGTH, MeasurementType.REPS, "reps",
     "Отжимания от пола"),
    ("Pull-ups", ExerciseCategory.STRENGTH, MeasurementType.REPS, "reps",
     "Подтягивания на турнике"),
    ("Squats", ExerciseCategory.STRENGTH, MeasurementType.REPS, "reps",
     "Приседания"),
    ("Plank", ExerciseCategory.CORE, MeasurementType.SECONDS, "seconds",
     "Планка на предплечьях"),
    ("Running", ExerciseCategory.CARDIO, MeasurementType.DISTANCE, "km",
     "Бег"),
]


def seed() -> None:
    """Создаёт базовые упражнения, если они отсутствуют."""
    db = SessionLocal()
    try:
        created = 0
        for name, category, mtype, unit, desc in BUILTIN_EXERCISES:
            existing = db.query(Exercise).filter_by(name=name).first()
            if existing is not None:
                continue
            db.add(Exercise(
                name=name,
                category=category,
                measurement_type=mtype,
                unit=unit,
                description=desc,
                is_custom=False,
            ))
            created += 1

        db.commit()
        print(f"Seeding complete: {created} exercises created, "
              f"{len(BUILTIN_EXERCISES) - created} already existed.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
