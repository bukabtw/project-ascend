"""Тесты API профиля (GET/PATCH /api/v1/profile)."""

from __future__ import annotations


def test_get_profile(client, registered_user):
    """GET /profile возвращает профиль зарегистрированного пользователя."""
    resp = client.get("/api/v1/profile", headers=registered_user["headers"])
    assert resp.status_code == 200
    data = resp.json()
    assert data["id"] == registered_user["id"]
    assert data["username"] == registered_user["username"]
    assert data["level"] == 1
    assert data["experience"] == 0
    assert "exp_to_next" in data
    assert data["exp_to_next"] > 0
    assert data["stats"]["strength"] == 1
    assert data["stats"]["endurance"] == 1
    assert data["stats"]["core"] == 1
    assert data["stats"]["recovery"] == 1


def test_patch_profile(client, registered_user):
    """PATCH /profile обновляет поля профиля."""
    resp = client.patch("/api/v1/profile", json={
        "display_name": "Игрок",
        "height_cm": 178.5,
        "goal_notes": "Достичь 83 кг",
    }, headers=registered_user["headers"])
    assert resp.status_code == 200
    data = resp.json()
    assert data["display_name"] == "Игрок"
    # height_cm не входит в ответ, но сохраняется в БД


def test_patch_profile_partial(client, registered_user):
    """PATCH /profile с одним полем не затрагивает остальные."""
    # Сначала устанавливаем display_name
    client.patch("/api/v1/profile", json={"display_name": "Имя1"},
                 headers=registered_user["headers"])
    # Затем обновляем только goal_notes
    resp = client.patch("/api/v1/profile", json={"goal_notes": "Цель"},
                        headers=registered_user["headers"])
    assert resp.status_code == 200
    data = resp.json()
    assert data["display_name"] == "Имя1"


def test_patch_profile_empty_body(client, registered_user):
    """PATCH /profile с пустым телом возвращает профиль без изменений."""
    resp = client.patch("/api/v1/profile", json={}, headers=registered_user["headers"])
    assert resp.status_code == 200
    assert resp.json()["id"] == registered_user["id"]
