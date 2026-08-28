"""Базовая конфигурация SQLAlchemy.

Импорт моделей в этом модуле регистрирует все таблицы в
``Base.metadata`` — это необходимо для Alembic и ``create_all``.
"""

from app.models.base import Base  # noqa: F401
from app.models.exercise import CalibrationRecord, Exercise  # noqa: F401
from app.models.game import (  # noqa: F401
    Achievement,
    Boss,
    Item,
    Lootbox,
    LootboxReward,
    UserAchievement,
    UserInventory,
)
from app.models.health import (  # noqa: F401
    HealthMetric,
    MetricDefinition,
    RawHealthImport,
    SyncLog,
)
from app.models.quest import DailyQuest, QuestCompletion, QuestTemplate  # noqa: F401
from app.models.readiness import ReadinessScore  # noqa: F401
from app.models.user import Profile, User  # noqa: F401
