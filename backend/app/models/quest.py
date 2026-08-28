"""Модели квестов: шаблоны, ежедневные квесты, выполнения (разделы 20-23, 33-34, 53-54 ТЗ)."""

from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import (
    Date,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin
from app.models.enums import CompletionSource, ExerciseCategory, QuestStatus, enum_values


class QuestTemplate(Base, TimestampMixin):
    """Шаблон задания — НЕ конкретный квест на сегодня (раздел 53 ТЗ)."""

    __tablename__ = "quest_templates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    exercise_id: Mapped[int | None] = mapped_column(
        ForeignKey("exercises.id", ondelete="SET NULL"), nullable=True
    )
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str | None] = mapped_column(String(512), nullable=True)
    category: Mapped[ExerciseCategory] = mapped_column(
        Enum(ExerciseCategory, values_callable=enum_values), nullable=False
    )
    base_value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String(32), nullable=False)
    base_exp: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[float] = mapped_column(Float, default=0.6, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    daily_quests: Mapped[list[DailyQuest]] = relationship(back_populates="template")


class DailyQuest(Base, TimestampMixin):
    """Сгенерированный квест на конкретный день (раздел 54 ТЗ).

    История сохраняется: изменение алгоритма генерации не затрагивает старые квесты.
    """

    __tablename__ = "daily_quests"
    __table_args__ = (
        Index("ix_daily_quests_user_date", "user_id", "date"),
        # Один шаблон не выдаётся дважды в день одному пользователю.
        UniqueConstraint("user_id", "date", "template_id", name="uq_daily_user_date_template"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    template_id: Mapped[int | None] = mapped_column(
        ForeignKey("quest_templates.id", ondelete="SET NULL"), nullable=True
    )
    date: Mapped[date] = mapped_column(Date, nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str | None] = mapped_column(String(512), nullable=True)
    category: Mapped[ExerciseCategory] = mapped_column(
        Enum(ExerciseCategory, values_callable=enum_values), nullable=False
    )
    target_value: Mapped[float] = mapped_column(Float, nullable=False)
    unit: Mapped[str] = mapped_column(String(32), nullable=False)
    exp_reward: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[QuestStatus] = mapped_column(
        Enum(QuestStatus, values_callable=enum_values),
        default=QuestStatus.PENDING,
        nullable=False,
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    template: Mapped[QuestTemplate | None] = relationship(back_populates="daily_quests")
    completion: Mapped[QuestCompletion | None] = relationship(
        back_populates="quest", uselist=False, cascade="all, delete-orphan"
    )


class QuestCompletion(Base):
    """Факт выполнения квеста (раздел 33 ТЗ)."""

    __tablename__ = "quest_completions"
    __table_args__ = (Index("ix_quest_completions_user_date", "user_id", "date"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    quest_id: Mapped[int | None] = mapped_column(
        ForeignKey("daily_quests.id", ondelete="SET NULL"), nullable=True
    )
    date: Mapped[date] = mapped_column(Date, nullable=False)
    planned_value: Mapped[float] = mapped_column(Float, nullable=False)
    actual_value: Mapped[float] = mapped_column(Float, nullable=False)
    exp_earned: Mapped[int] = mapped_column(Integer, nullable=False)
    modifier: Mapped[float] = mapped_column(Float, default=1.0, nullable=False)
    source: Mapped[CompletionSource] = mapped_column(
        Enum(CompletionSource, values_callable=enum_values),
        default=CompletionSource.MANUAL,
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )

    quest: Mapped[DailyQuest | None] = relationship(back_populates="completion")
