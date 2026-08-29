"""Тесты API упражнений и калибровки (разделы 24-26 ТЗ)."""

from __future__ import annotations

from datetime import datetime


def test_list_exercises_empty(client, registered_user):
    """Список упражнений пуст до сидинга."""
    resp = client.get("/api/v1/exercises", headers=registered_user["headers"])
    assert resp.status_code == 200
    assert resp.json() == []


def test_create_custom_exercise(client, registered_user):
    """Создание пользовательского упражнения."""
    resp = client.post("/api/v1/exercises", json={
        "name": "Dumbbell Curls",
        "category": "strength",
        "measurement_type": "reps",
        "unit": "reps",
        "description": "Подъём гантелей на бицепс",
    }, headers=registered_user["headers"])
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Dumbbell Curls"
    assert data["is_custom"] is True
    assert data["created_by"] == registered_user["id"]
    assert data["category"] == "strength"


def test_create_exercise_duplicate(client, registered_user):
    """Создание упражнения с существующим именем — 409."""
    body = {
        "name": "Lunges",
        "category": "strength",
        "measurement_type": "reps",
        "unit": "reps",
    }
    client.post("/api/v1/exercises", json=body, headers=registered_user["headers"])
    resp = client.post("/api/v1/exercises", json=body, headers=registered_user["headers"])
    assert resp.status_code == 409


def test_create_calibration(client, registered_user):
    """Создание калибровочной записи."""
    # Сначала создаём упражнение
    ex = client.post("/api/v1/exercises", json={
        "name": "Push-ups",
        "category": "strength",
        "measurement_type": "reps",
        "unit": "reps",
    }, headers=registered_user["headers"]).json()

    resp = client.post("/api/v1/calibration", json={
        "exercise_id": ex["id"],
        "value": 30,
        "unit": "reps",
        "performed_at": "2026-08-28T09:00:00",
        "notes": "строгая форма",
    }, headers=registered_user["headers"])
    assert resp.status_code == 201
    data = resp.json()
    assert data["value"] == 30
    assert data["exercise_name"] == "Push-ups"
    assert data["unit"] == "reps"


def test_create_calibration_nonexistent_exercise(client, registered_user):
    """Калибровка с несуществующим exercise_id — 404."""
    resp = client.post("/api/v1/calibration", json={
        "exercise_id": 9999,
        "value": 10,
        "unit": "reps",
        "performed_at": datetime.now().isoformat(),
    }, headers=registered_user["headers"])
    assert resp.status_code == 404


def test_list_calibrations(client, registered_user):
    """Список калибровочных записей."""
    ex = client.post("/api/v1/exercises", json={
        "name": "Squats",
        "category": "strength",
        "measurement_type": "reps",
        "unit": "reps",
    }, headers=registered_user["headers"]).json()

    client.post("/api/v1/calibration", json={
        "exercise_id": ex["id"],
        "value": 50,
        "unit": "reps",
        "performed_at": "2026-08-28T09:00:00",
    }, headers=registered_user["headers"])

    resp = client.get("/api/v1/calibration", headers=registered_user["headers"])
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["exercise_name"] == "Squats"


def test_list_calibrations_filter(client, registered_user):
    """Фильтрация калибровок по exercise_id."""
    ex1 = client.post("/api/v1/exercises", json={
        "name": "Pull-ups", "category": "strength",
        "measurement_type": "reps", "unit": "reps",
    }, headers=registered_user["headers"]).json()
    ex2 = client.post("/api/v1/exercises", json={
        "name": "Plank", "category": "core",
        "measurement_type": "seconds", "unit": "seconds",
    }, headers=registered_user["headers"]).json()

    for ex_id, val in [(ex1["id"], 10), (ex2["id"], 60)]:
        client.post("/api/v1/calibration", json={
            "exercise_id": ex_id, "value": val,
            "unit": "reps" if val == 10 else "seconds",
            "performed_at": "2026-08-28T09:00:00",
        }, headers=registered_user["headers"])

    resp = client.get(f"/api/v1/calibration?exercise_id={ex1['id']}",
                      headers=registered_user["headers"])
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["exercise_name"] == "Pull-ups"
