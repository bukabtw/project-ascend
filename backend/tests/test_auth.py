"""Тесты регистрации и аутентификации (раздел 56 ТЗ)."""

from __future__ import annotations


def test_register_success(client):
    """Успешная регистрация создаёт пользователя с уровнем 1."""
    resp = client.post("/api/v1/users/register", json={
        "username": "newplayer",
        "password": "password123",
    })
    assert resp.status_code == 201
    data = resp.json()
    assert data["username"] == "newplayer"
    assert data["level"] == 1
    assert data["experience"] == 0
    assert "id" in data
    assert "created_at" in data
    # Пароль не возвращается
    assert "password" not in data
    assert "password_hash" not in data


def test_register_duplicate_username(client, registered_user):
    """Повторная регистрация с тем же username — 409."""
    resp = client.post("/api/v1/users/register", json={
        "username": registered_user["username"],
        "password": "other456",
    })
    assert resp.status_code == 409


def test_register_short_password(client):
    """Пароль короче 6 символов — 422."""
    resp = client.post("/api/v1/users/register", json={
        "username": "shortpw",
        "password": "12345",
    })
    assert resp.status_code == 422


def test_register_short_username(client):
    """Username короче 3 символов — 422."""
    resp = client.post("/api/v1/users/register", json={
        "username": "ab",
        "password": "password123",
    })
    assert resp.status_code == 422


def test_profile_without_header(client):
    """GET /profile без заголовка X-Ascend-User — 401."""
    resp = client.get("/api/v1/profile")
    assert resp.status_code == 401


def test_profile_invalid_header(client):
    """GET /profile с нечисловым заголовком — 401."""
    resp = client.get("/api/v1/profile", headers={"X-Ascend-User": "abc"})
    assert resp.status_code == 401


def test_profile_nonexistent_user(client):
    """GET /profile с ID несуществующего пользователя — 403."""
    resp = client.get("/api/v1/profile", headers={"X-Ascend-User": "9999"})
    assert resp.status_code == 403
