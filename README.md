# Ascend

**Система персонального ИИ-тренера и геймификации здоровья.**

Ascend превращает регулярные тренировки, физическую активность и контроль
состояния организма в RPG-систему. Система собирает данные о активности и
состоянии пользователя, анализирует их, определяет готовность к нагрузке
и формирует персональные ежедневные квесты, за выполнение которых
пользователь получает опыт, повышает уровень и развивает характеристики.

> Проект не является медицинской системой и не предназначен для диагностики
> заболеваний. Показатели состояния используются исключительно для адаптации
> тренировочной нагрузки.

---

## Возможности

- **Калибровка** — первичное физическое тестирование пользователя.
- **HealthSync** — импорт данных из Apple Health (XML/JSON/CSV), ручной ввод,
  неизменяемое хранение исходных данных и перепроцессинг.
- **Readiness Engine** — оценка готовности к нагрузке (0–100) на основе сна,
  пульса покоя, активности, тренировочной нагрузки и восстановления.
- **Quest Engine** — генерация адаптивных ежедневных квестов (Strength / Core /
  Cardio / Recovery) с учётом готовности, уровня и истории.
- **Game Engine** — опыт, уровни, характеристики, боссы, достижения, лут.
- **Desktop Client** (PyQt6) — Dashboard, Quests, Profile, Progress, Bosses,
  Achievements, Inventory, Health, Import, Settings.
- **Telegram Bot** (aiogram) — `/daily`, `/done`, `/status`, `/readiness`,
  `/bosses`, `/achievements`.
- **Экспорт и backup** — CSV/JSON-экспорт и `.ascend-backup`.

---

## Технологический стек

| Слой          | Технологии                                            |
|---------------|-------------------------------------------------------|
| Backend       | Python 3.10+, FastAPI, Uvicorn, Pydantic, SQLAlchemy  |
| Миграции      | Alembic                                               |
| База данных   | SQLite (local-first)                                  |
| Desktop       | PyQt6, matplotlib / pyqtgraph                         |
| Telegram      | aiogram 3.x                                           |
| Тестирование  | pytest, pytest-asyncio, httpx TestClient              |
| Качество кода | Ruff, Black, mypy, pre-commit                         |

---

## Архитектура

Ascend построен вокруг универсальной цепочки:

```
DATA → INTERPRETATION → STATE → DECISION → ACTION → PROGRESS
```

Ключевые принципы: **local-first**, разделение исходных и обработанных данных,
независимость от источников, offline-first.

Подробности — в документации:

- [`docs/architecture.md`](docs/architecture.md) — архитектура и компоненты
- [`docs/er-diagram.md`](docs/er-diagram.md) — ER-диаграмма (19 таблиц)
- [`docs/api-contract.md`](docs/api-contract.md) — API-контракт v1
- [`specs.md`](specs.md) — полное техническое задание

```
Desktop Client / Telegram Bot
        │
        ▼
   FastAPI Application
        │
  ┌─────┼─────┐
  ▼     ▼     ▼
HealthSync  Readiness  Quest Engine  →  Game Engine
  │         Engine
  └─────────┴──────────► SQLite
```

---

## Структура проекта

```
ascend/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI роутеры и зависимости
│   │   ├── core/         # конфигурация (config.py)
│   │   ├── db/           # engine, session, Base
│   │   ├── models/       # SQLAlchemy ORM-модели (19 таблиц)
│   │   ├── schemas/      # Pydantic-схемы API
│   │   ├── services/     # healthsync, readiness, quests, game
│   │   └── main.py       # точка входа FastAPI
│   └── tests/
├── desktop/              # PyQt6 клиент (Sprint 7)
├── telegram/             # aiogram бот (Sprint 8)
├── migrations/           # Alembic (Sprint 1)
├── docs/                 # архитектура, ER, API-контракт
├── exports/              # экспорт CSV/JSON
├── backups/              # резервные копии
├── pyproject.toml
├── .env.example
└── specs.md
```

---

## Быстрый старт

### 1. Клонирование и окружение

```bash
git clone <repo-url> ascend
cd ascend

python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate
```

### 2. Установка зависимостей

```bash
pip install -e ".[dev]"
# Дополнительно (по мере реализации спринтов):
pip install -e ".[telegram]"   # aiogram (Sprint 8)
pip install -e ".[desktop]"    # PyQt6 (Sprint 7)
```

### 3. Конфигурация

```bash
cp .env.example .env
# Отредактируйте .env: SECRET_KEY, DATABASE_URL и т.д.
```

### 4. Запуск backend

```bash
# Из директории backend:
cd backend
uvicorn app.main:app --reload
```

API будет доступен на `http://127.0.0.1:8000`, документация — на `/docs`.

Проверка работоспособности:

```bash
curl http://127.0.0.1:8000/api/v1/health
# {"status":"ok"}
```

---

## Разработка

### Линтинг и форматирование

```bash
ruff check backend/
black backend/
mypy backend/
```

### Тесты

```bash
pytest
```

### Создание таблиц (временно, до Alembic в Sprint 1)

```python
from app.db.base import Base
from app.db.session import engine
Base.metadata.create_all(engine)
```

---

## Дорожная карта

| Спринт | Содержание                         | Статус       |
|--------|------------------------------------|--------------|
| 0      | Проектирование: структура, модели, конфигурация, ER, API-контракт | ✅ Готов |
| 1      | Database + Backend Core (Alembic, API) | ⏳ План   |
| 2      | Калибровка                         | ⏳ План       |
| 3      | HealthSync (импорт, интерпретация) | ⏳ План       |
| 4      | Readiness Engine                   | ⏳ План       |
| 5      | Quest Engine                       | ⏳ План       |
| 6      | Game Engine                        | ⏳ План       |
| 7      | Desktop (PyQt6)                    | ⏳ План       |
| 8      | Telegram Bot                       | ⏳ План       |
| 9      | Analytics, экспорт                 | ⏳ План       |
| 10     | Reliability (тесты, backup, логи)  | ⏳ План       |
| 11     | Release (упаковка, документация)   | ⏳ План       |

Полный список этапов — в [`specs.md`](specs.md), раздел 74.

---

## Безопасность

- Пароли хранятся только в виде хэша (password hashing).
- Секреты (`SECRET_KEY`, `TELEGRAM_BOT_TOKEN`) — только в окружении, не в БД.
- API валидирует запросы и проверяет принадлежность объектов пользователю.
- Доступ Telegram Bot ограничен (раздел 56 ТЗ).

---

## Лицензия

Proprietary. © Ascend Team.