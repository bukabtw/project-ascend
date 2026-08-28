# API-контракт Ascend (v1)

> Базовый префикс всех endpoints: `/api/v1`.
> Полный список — в [`specs.md`](../specs.md), раздел 49.

## Соглашения

### Аутентификация

Локальное приложение использует заголовок для идентификации пользователя:

```
X-Ascend-User: <user_id>
```

(Механизм аутентификации с паролями/токенами вводится в Sprint 1; до этого
для локального режима достаточно идентификатора пользователя.)

### Формат ошибок

Все ошибки возвращаются в едином формате (FastAPI default):

```json
{ "detail": "Описание ошибки" }
```

HTTP-коды: `400` — ошибка валидации/бизнес-логики, `404` — не найдено,
`422` — ошибка Pydantic-схемы, `500` — внутренняя ошибка.

---

## Profile

### `GET /api/v1/profile`

Возвращает профиль и игровые характеристики текущего пользователя.

**Response 200:**
```json
{
  "id": 1,
  "username": "player",
  "display_name": "Игрок",
  "level": 24,
  "experience": 1240,
  "exp_to_next": 1500,
  "stats": {
    "strength": 37,
    "endurance": 42,
    "core": 29,
    "recovery": 34
  },
  "created_at": "2026-01-15T10:00:00"
}
```

### `PATCH /api/v1/profile`

Обновляет редактируемые поля профиля.

**Body:**
```json
{ "display_name": "Новое имя", "height_cm": 178.0 }
```

---

## Calibration

### `POST /api/v1/calibration`

Сохраняет результат калибровочного теста (раздел 24 ТЗ).

**Body:**
```json
{
  "exercise_id": 2,
  "value": 30,
  "unit": "reps",
  "performed_at": "2026-08-28T09:00:00",
  "notes": "отжимания, строгая форма"
}
```

**Response 201:** созданная `CalibrationRecord` + пересчитанные стартовые характеристики.

### `GET /api/v1/calibration`

Возвращает историю калибровочных записей.

**Query:** `?exercise_id=` (опционально)

---

## Health

### `POST /api/v1/health/import`

Загружает файл импорта (XML/JSON/CSV). Сохраняет Raw Import (раздел 8 ТЗ),
определяет формат по содержимому, вычисляет `file_hash` (SHA-256) и проверяет
идемпотентность.

**Body:** `multipart/form-data` с полем `file`.

**Response 201:**
```json
{
  "import_id": 42,
  "source": "apple_health",
  "format": "xml",
  "file_hash": "a1b2c3...",
  "status": "pending",
  "records_found": 1280
}
```
**Response 200 (дубликат):** `{ "import_id": 42, "status": "duplicate" }`

### `POST /api/v1/health/interpret/{import_id}`

Запускает интерпретацию существующего Raw Import (раздел 15 — перепроцессинг).
Создаёт/обновляет `health_metrics`, пишет ошибки в `sync_logs`.

**Response 200:**
```json
{
  "import_id": 42,
  "metrics_created": 980,
  "errors": 12,
  "status": "parsed"
}
```

### `GET /api/v1/health/metrics`

Возвращает нормализованные метрики.

**Query:** `?metric_type=weight&from=2026-08-01&to=2026-08-28&limit=100`

**Response 200:**
```json
{
  "items": [
    {
      "id": 1,
      "metric_type": "weight",
      "value": 83.2,
      "unit": "kg",
      "timestamp": "2026-08-28T07:30:00",
      "source": "apple_health"
    }
  ],
  "total": 1
}
```

### `GET /api/v1/health/readiness`

Возвращает текущий/исторический Readiness Score (раздел 16 ТЗ).

**Query:** `?date=2026-08-28` (по умолчанию — сегодня)

**Response 200:**
```json
{
  "date": "2026-08-28",
  "score": 73,
  "band": "good",
  "training_modifier": 0.85,
  "reason": "short_sleep"
}
```

---

## Quests

### `GET /api/v1/quests/daily`

Возвращает (или генерирует при отсутствии) ежедневные квесты.

**Query:** `?date=2026-08-28`

**Response 200:**
```json
{
  "date": "2026-08-28",
  "readiness": 78,
  "quests": [
    {
      "id": 1,
      "name": "Отжимания",
      "category": "strength",
      "target_value": 30,
      "unit": "reps",
      "exp_reward": 15,
      "difficulty": 0.6,
      "status": "pending"
    }
  ]
}
```

### `POST /api/v1/quests/{quest_id}/complete`

Отмечает квест выполненным (раздел 33 ТЗ).

**Body:**
```json
{ "actual_value": 35, "source": "manual" }
```

**Response 200:**
```json
{
  "quest_id": 1,
  "exp_earned": 15,
  "stat_gains": { "strength": 2 },
  "new_level": null
}
```

### `GET /api/v1/quests/history`

История выполненных квестов.

**Query:** `?from=&to=&category=`

---

## Game

### `GET /api/v1/game/status`

Игровой статус пользователя.

**Response 200:**
```json
{
  "level": 24,
  "experience": 1240,
  "exp_to_next": 1500,
  "stats": { "strength": 37, "endurance": 42, "core": 29, "recovery": 34 },
  "streak": 5
}
```

### `GET /api/v1/game/inventory`

Инвентарь пользователя.

### `POST /api/v1/game/lootbox/claim`

Открывает доступный лутбокс и возвращает выпавшую награду (раздел 35 ТЗ).

**Response 200:**
```json
{ "item": { "id": 7, "name": "Бонус +10% EXP", "item_type": "temporary_bonus" } }
```

---

## Bosses

### `GET /api/v1/bosses`

Список боссов пользователя (активные и побеждённые).

**Response 200:**
```json
{
  "items": [
    {
      "id": 1,
      "name": "Достичь 83 кг",
      "target_type": "weight",
      "target_value": 83.0,
      "current_value": 85.4,
      "progress": 0.76,
      "is_defeated": false
    }
  ]
}
```

### `POST /api/v1/bosses`

Создаёт нового босса.

**Body:**
```json
{
  "name": "15 подтягиваний",
  "target_type": "exercise",
  "target_value": 15,
  "reward_id": null
}
```

### `PATCH /api/v1/bosses/{boss_id}`

Обновляет прогресс/статус босса.

**Body:** `{ "current_value": 12 }`

---

## Achievements

### `GET /api/v1/achievements`

Доступные и полученные достижения (раздел 36 ТЗ).

**Response 200:**
```json
{
  "items": [
    {
      "code": "first_quest",
      "name": "Первый квест",
      "description": "Выполните первый квест",
      "unlocked_at": "2026-08-20T18:00:00"
    }
  ]
}
```

---

## Export

### `GET /api/v1/export/csv`

Выгрузка данных в CSV (раздел 61 ТЗ).

**Query:** `?section=health_metrics|quests|game` (опционально)

**Response 200:** `text/csv` (attachment)

### `GET /api/v1/export/json`

Полный экспорт данных в JSON.

**Response 200:** `application/json` (attachment)

---

## Системные endpoints

| Метод | Endpoint                | Описание                          |
|-------|-------------------------|-----------------------------------|
| GET   | `/`                     | Информация о приложении           |
| GET   | `/api/v1/health`        | Healthcheck API                   |
| GET   | `/api/v1/openapi.json`  | OpenAPI-схема                     |
| GET   | `/docs`                 | Swagger UI                        |
| GET   | `/redoc`                | ReDoc                             |