"""Все ORM-модели Ascend.

Импорт этого пакета регистрирует все таблицы в ``Base.metadata``.
"""

from app.models.base import Base, TimestampMixin
from app.models.enums import (
    BossTargetType,
    CompletionSource,
    ExerciseCategory,
    ImportStatus,
    ItemType,
    MeasurementType,
    MetricType,
    QuestStatus,
    SyncLogLevel,
)
from app.models.exercise import CalibrationRecord, Exercise
from app.models.game import (
    Achievement,
    Boss,
    Item,
    Lootbox,
    LootboxReward,
    UserAchievement,
    UserInventory,
)
from app.models.health import (
    HealthMetric,
    MetricDefinition,
    RawHealthImport,
    SyncLog,
)
from app.models.quest import DailyQuest, QuestCompletion, QuestTemplate
from app.models.readiness import ReadinessScore
from app.models.user import Profile, User

__all__ = [
    "Achievement",
    "Base",
    "Boss",
    "BossTargetType",
    "CalibrationRecord",
    "CompletionSource",
    "DailyQuest",
    "Exercise",
    "ExerciseCategory",
    "HealthMetric",
    "ImportStatus",
    "Item",
    "ItemType",
    "Lootbox",
    "LootboxReward",
    "MeasurementType",
    "MetricDefinition",
    "MetricType",
    "Profile",
    "QuestCompletion",
    "QuestStatus",
    "QuestTemplate",
    "RawHealthImport",
    "ReadinessScore",
    "SyncLog",
    "SyncLogLevel",
    "TimestampMixin",
    "User",
    "UserAchievement",
    "UserInventory",
]
