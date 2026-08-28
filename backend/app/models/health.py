"""Модели HealthSync: импорты, метрики, справочник метрик, логи (разделы 7-14, 52 ТЗ)."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import (
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin
from app.models.enums import ImportStatus, MetricType, SyncLogLevel, enum_values


class MetricDefinition(Base, TimestampMixin):
    """Справочник допустимых типов метрик и их базовых единиц (раздел 11 ТЗ).

    Предотвращает появление некорректных комбинаций ``metric_type`` + ``unit``.
    """

    __tablename__ = "metric_definitions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    metric_type: Mapped[MetricType] = mapped_column(
        Enum(MetricType, values_callable=enum_values),
        unique=True,
        index=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    base_unit: Mapped[str] = mapped_column(String(32), nullable=False)
    description: Mapped[str | None] = mapped_column(String(256), nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)


class RawHealthImport(Base):
    """Неизменяемое хранилище исходных данных импорта (раздел 8 ТЗ).

    Raw-данные сохраняются без изменений и не зависят от логики интерпретации.
    """

    __tablename__ = "raw_health_imports"
    __table_args__ = (
        # Идемпотентность (раздел 8.3): один файл — одна запись на пользователя.
        UniqueConstraint("user_id", "file_hash", name="uq_imports_user_hash"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    source: Mapped[str] = mapped_column(String(64), nullable=False)
    file_name: Mapped[str] = mapped_column(String(256), nullable=False)
    file_hash: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    format: Mapped[str] = mapped_column(String(16), nullable=False)
    raw_data: Mapped[str | None] = mapped_column(Text, nullable=True)
    imported_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    status: Mapped[ImportStatus] = mapped_column(
        Enum(ImportStatus, values_callable=enum_values),
        default=ImportStatus.PENDING,
        nullable=False,
    )

    metrics: Mapped[list[HealthMetric]] = relationship(
        back_populates="raw_import", cascade="all, delete-orphan"
    )


class HealthMetric(Base):
    """Нормализованная метрика пользователя (раздел 12 ТЗ)."""

    __tablename__ = "health_metrics"
    __table_args__ = (
        Index("ix_health_metrics_user_ts", "user_id", "timestamp"),
        Index("ix_health_metrics_user_metric_ts", "user_id", "metric_type", "timestamp"),
        Index("ix_health_metrics_metric", "metric_type"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    # import_id nullable: ручной ввод не связан с Raw Import.
    import_id: Mapped[int | None] = mapped_column(
        ForeignKey("raw_health_imports.id", ondelete="CASCADE"), index=True, nullable=True
    )
    timestamp: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    metric_type: Mapped[MetricType] = mapped_column(
        Enum(MetricType, values_callable=enum_values), nullable=False
    )
    value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String(32), nullable=False)
    source: Mapped[str] = mapped_column(String(64), nullable=False)
    raw_data: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

    raw_import: Mapped[RawHealthImport | None] = relationship(back_populates="metrics")


class SyncLog(Base):
    """Лог синхронизации/интерпретации данных (раздел 52 ТЗ)."""

    __tablename__ = "sync_logs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=True
    )
    import_id: Mapped[int | None] = mapped_column(
        ForeignKey("raw_health_imports.id", ondelete="CASCADE"), index=True, nullable=True
    )
    level: Mapped[SyncLogLevel] = mapped_column(
        Enum(SyncLogLevel, values_callable=enum_values), nullable=False
    )
    message: Mapped[str] = mapped_column(String(512), nullable=False)
    details: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
