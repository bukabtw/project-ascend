"""Общие фикстуры pytest для Ascend.

Использует in-memory SQLite, чтобы тесты были изолированными и быстрыми.
"""

from __future__ import annotations

from collections.abc import Generator

import pytest
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool


@pytest.fixture(scope="function")
def db_engine():
    """In-memory SQLite engine со всеми таблицами (создаётся на каждый тест).

    ``StaticPool`` гарантирует, что все соединения используют один и тот же
    in-memory database (по умолчанию каждое соединение получает свою копию).
    """
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(db_engine) -> Generator[Session, None, None]:
    """Сессия БД для тестов."""
    TestSessionLocal = sessionmaker(bind=db_engine, autocommit=False, autoflush=False, future=True)
    session = TestSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope="function")
def client(db_session) -> Generator[TestClient, None, None]:
    """TestClient с подменённой БД (in-memory)."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture()
def registered_user(client) -> dict:
    """Регистрирует пользователя и возвращает его данные + заголовок."""
    resp = client.post("/api/v1/users/register", json={
        "username": "testuser",
        "password": "secret123",
    })
    assert resp.status_code == 201, resp.text
    data = resp.json()
    return {
        "id": data["id"],
        "username": data["username"],
        "headers": {"X-Ascend-User": str(data["id"])},
    }
