"""Перечисления предметной области Ascend.

Значения перечислений хранятся в БД в нижнем регистре (через
``values_callable``), что соответствует примерам в ТЗ
(например ``status = "manual"``, ``source = "auto"``).
"""

from __future__ import annotations

import enum


def enum_values(enum_cls: type[enum.Enum]) -> list[str]:
    """Возвращает список значений перечисления для хранения в БД."""
    return [member.value for member in enum_cls]


class ImportStatus(str, enum.Enum):
    """Статус обработки Raw Import (раздел 8 ТЗ)."""

    PENDING = "pending"
    PARSED = "parsed"
    ERROR = "error"
    DELETED = "deleted"


class SyncLogLevel(str, enum.Enum):
    """Уровни лога синхронизации (раздел 52 ТЗ)."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class MetricType(str, enum.Enum):
    """Типы метрик Ascend (разделы 9.2, 11 ТЗ)."""

    WEIGHT = "weight"
    BODY_FAT = "body_fat"
    RESTING_HR = "resting_hr"
    SLEEP = "sleep"
    STEPS = "steps"
    DISTANCE = "distance"
    ACTIVE_ENERGY = "active_energy"
    VO2MAX = "vo2max"


class ExerciseCategory(str, enum.Enum):
    """Категории упражнений и квестов (раздел 21 ТЗ)."""

    STRENGTH = "strength"
    CORE = "core"
    CARDIO = "cardio"
    RECOVERY = "recovery"


class MeasurementType(str, enum.Enum):
    """Способ измерения упражнения (раздел 26 ТЗ)."""

    REPS = "reps"
    SECONDS = "seconds"
    DISTANCE = "distance"
    WEIGHT = "weight"
    DURATION = "duration"


class QuestStatus(str, enum.Enum):
    """Статус ежедневного квеста (разделы 33-34 ТЗ)."""

    PENDING = "pending"
    COMPLETED = "completed"
    AUTO_COMPLETED = "auto_completed"
    SKIPPED = "skipped"


class CompletionSource(str, enum.Enum):
    """Источник выполнения квеста (раздел 33 ТЗ)."""

    MANUAL = "manual"
    AUTO = "auto"


class BossTargetType(str, enum.Enum):
    """Тип цели босса (раздел 31 ТЗ)."""

    WEIGHT = "weight"
    EXERCISE = "exercise"
    DISTANCE = "distance"
    STREAK = "streak"
    QUESTS = "quests"


class ItemType(str, enum.Enum):
    """Типы игровых предметов / наград (раздел 35 ТЗ)."""

    EXP = "exp"
    STAT_POINTS = "stat_points"
    COSMETIC = "cosmetic"
    TEMPORARY_BONUS = "temporary_bonus"
    SPECIAL = "special"
