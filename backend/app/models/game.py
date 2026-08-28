"""Игровые модели: боссы, достижения, предметы, лутбоксы, инвентарь (разделы 31-36 ТЗ)."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import (
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin
from app.models.enums import BossTargetType, ItemType, enum_values


class Item(Base, TimestampMixin):
    """Игровой предмет / тип награды (раздел 35 ТЗ)."""

    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    description: Mapped[str | None] = mapped_column(String(512), nullable=True)
    item_type: Mapped[ItemType] = mapped_column(
        Enum(ItemType, values_callable=enum_values), nullable=False
    )


class Lootbox(Base, TimestampMixin):
    """Лутбокс — контейнер случайных наград (раздел 35 ТЗ)."""

    __tablename__ = "lootboxes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str | None] = mapped_column(String(512), nullable=True)

    rewards: Mapped[list[LootboxReward]] = relationship(
        back_populates="lootbox", cascade="all, delete-orphan"
    )


class LootboxReward(Base):
    """Возможная награда из лутбокса с вероятностью выпадения."""

    __tablename__ = "lootbox_rewards"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    lootbox_id: Mapped[int] = mapped_column(
        ForeignKey("lootboxes.id", ondelete="CASCADE"), index=True, nullable=False
    )
    item_id: Mapped[int] = mapped_column(
        ForeignKey("items.id", ondelete="CASCADE"), index=True, nullable=False
    )
    probability: Mapped[float] = mapped_column(Float, nullable=False)

    lootbox: Mapped[Lootbox] = relationship(back_populates="rewards")


class UserInventory(Base):
    """Инвентарь пользователя (раздел 50 ТЗ)."""

    __tablename__ = "user_inventory"
    __table_args__ = (
        UniqueConstraint("user_id", "item_id", name="uq_inventory_user_item"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    item_id: Mapped[int] = mapped_column(
        ForeignKey("items.id", ondelete="CASCADE"), index=True, nullable=False
    )
    quantity: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    acquired_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )


class Boss(Base, TimestampMixin):
    """Долгосрочная цель пользователя (раздел 32 ТЗ)."""

    __tablename__ = "bosses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str | None] = mapped_column(String(512), nullable=True)
    target_type: Mapped[BossTargetType] = mapped_column(
        Enum(BossTargetType, values_callable=enum_values), nullable=False
    )
    target_value: Mapped[float] = mapped_column(Float, nullable=False)
    current_value: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    is_defeated: Mapped[bool] = mapped_column(default=False, nullable=False)
    defeated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    reward_id: Mapped[int | None] = mapped_column(
        ForeignKey("items.id", ondelete="SET NULL"), nullable=True
    )


class Achievement(Base, TimestampMixin):
    """Достижение с условием получения (раздел 36 ТЗ)."""

    __tablename__ = "achievements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str | None] = mapped_column(String(512), nullable=True)
    condition: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    reward_id: Mapped[int | None] = mapped_column(
        ForeignKey("items.id", ondelete="SET NULL"), nullable=True
    )


class UserAchievement(Base):
    """Полученное пользователем достижение (раздел 36 ТЗ)."""

    __tablename__ = "user_achievements"
    __table_args__ = (
        UniqueConstraint("user_id", "achievement_id", name="uq_user_achievement"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False
    )
    achievement_id: Mapped[int] = mapped_column(
        ForeignKey("achievements.id", ondelete="CASCADE"), index=True, nullable=False
    )
    unlocked_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
