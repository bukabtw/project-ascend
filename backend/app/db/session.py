"""Создание engine и фабрики сессий SQLAlchemy."""

from __future__ import annotations

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings

settings = get_settings()

engine_kwargs: dict = {}
if settings.database_url.startswith("sqlite"):
    # SQLite может использоваться из нескольких потоков (FastAPI/uvicorn,
    # PyQt6) — отключаем проверку принадлежности потока.
    engine_kwargs["connect_args"] = {"check_same_thread": False}

engine = create_engine(settings.database_url, echo=settings.debug, future=True, **engine_kwargs)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)


def get_db() -> Generator[Session, None, None]:
    """FastAPI-зависимость: передаёт сессию БД в обработчик запроса."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
