"""Конфигурация приложения Ascend.

Все параметры баланса и поведения выносятся в конфигурацию (раздел 57 ТЗ),
что позволяет изменять значения в .env без переписывания бизнес-логики.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Корень проекта: backend/app/core/config.py -> ascend/
PROJECT_ROOT: Path = Path(__file__).resolve().parents[3]

DEFAULT_READINESS_WEIGHTS: dict[str, float] = {
    "sleep": 0.25,
    "resting_hr": 0.20,
    "training_load": 0.20,
    "recovery": 0.20,
    "activity": 0.15,
}

DEFAULT_QUEST_DIFFICULTY_MODIFIERS: dict[str, float] = {
    "base": 0.6,
    "low_readiness": 0.5,
    "high_readiness": 1.1,
    "max": 1.0,
}


class Settings(BaseSettings):
    """Настройки приложения.

    Значения переопределяются переменными окружения и файлом `.env`
    в корне проекта (переменные окружения имеют приоритет).
    """

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # --- Общее ---
    app_name: str = "Ascend"
    app_version: str = "0.1.0"
    app_env: str = "development"
    api_prefix: str = "/api/v1"
    debug: bool = False

    # --- База данных ---
    database_url: str = "sqlite:///./ascend.db"

    # --- Безопасность (раздел 56 ТЗ) ---
    secret_key: str = "change-me-in-production"
    # Хранится ТОЛЬКО в окружении, не в базе данных.
    telegram_bot_token: str = Field(default="", repr=False)

    # --- Пути ---
    data_dir: Path = PROJECT_ROOT / "data"
    export_dir: Path = PROJECT_ROOT / "exports"
    backup_dir: Path = PROJECT_ROOT / "backups"
    log_dir: Path = PROJECT_ROOT / "logs"

    # --- EXP и уровни (разделы 28-29 ТЗ) ---
    # EXP, необходимый для перехода с уровня 1 на уровень 2.
    exp_base: int = 100
    # EXP_next = EXP_base * level_multiplier^(level - 1)
    level_multiplier: float = 1.2
    # Глобальный множитель получаемого опыта.
    exp_multiplier: float = 1.0

    # --- Readiness Engine (разделы 16-18, 57 ТЗ) ---
    # Веса факторов Readiness (сумма должна равняться 1.0).
    readiness_weights: dict[str, float] = DEFAULT_READINESS_WEIGHTS
    # Границы диапазонов готовности (раздел 16.1 ТЗ).
    # Диапазоны: 0-20 critical, 21-40 low, 41-60 medium, 61-80 good, 81-100 high.
    readiness_band_critical: int = 20
    readiness_band_low: int = 40
    readiness_band_medium: int = 60
    readiness_band_good: int = 80
    # Ниже этого значения нагрузка снижается (раздел 23 ТЗ).
    low_readiness_threshold: int = 40
    # Порог нагрузки, после которого включается recovery period (раздел 72 ТЗ).
    recovery_threshold: float = 0.85

    # --- Quest Engine (разделы 22-23, 57 ТЗ) ---
    # Модификаторы сложности квестов.
    quest_difficulty_modifiers: dict[str, float] = DEFAULT_QUEST_DIFFICULTY_MODIFIERS

    # --- Telegram (Sprint 8) ---
    telegram_allowed_user_ids: list[int] = Field(default_factory=list)

    @property
    def readiness_bands(self) -> list[tuple[int, int, str]]:
        """Диапазоны готовности в виде [(нижняя, верхняя, название), ...]."""
        return [
            (0, self.readiness_band_critical, "critical"),
            (self.readiness_band_critical + 1, self.readiness_band_low, "low"),
            (self.readiness_band_low + 1, self.readiness_band_medium, "medium"),
            (self.readiness_band_medium + 1, self.readiness_band_good, "good"),
            (self.readiness_band_good + 1, 100, "high"),
        ]

    def ensure_dirs(self) -> None:
        """Создаёт рабочие директории приложения, если их ещё нет."""
        for directory in (self.data_dir, self.export_dir, self.backup_dir, self.log_dir):
            directory.mkdir(parents=True, exist_ok=True)


@lru_cache
def get_settings() -> Settings:
    """Возвращает singleton настроек приложения."""
    return Settings()
