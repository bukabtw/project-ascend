# ER-диаграмма Ascend

> Полный текст ТЗ — в [`specs.md`](../specs.md). Диаграмма отражает схему
> из 19 таблиц, реализованную в Sprint 0 (`backend/app/models/`).

## Диаграмма связей

```mermaid
erDiagram
    USERS ||--o| PROFILES : "1:1 профиль"
    USERS ||--o{ RAW_HEALTH_IMPORTS : "импорты"
    USERS ||--o{ HEALTH_METRICS : "метрики"
    USERS ||--o{ SYNC_LOGS : "логи"
    USERS ||--o{ CALIBRATION_RECORDS : "калибровка"
    USERS ||--o{ DAILY_QUESTS : "квесты дня"
    USERS ||--o{ QUEST_COMPLETIONS : "выполнения"
    USERS ||--o{ READINESS_SCORES : "готовность"
    USERS ||--o{ BOSSES : "боссы"
    USERS ||--o{ USER_ACHIEVEMENTS : "достижения"
    USERS ||--o{ USER_INVENTORY : "инвентарь"

    RAW_HEALTH_IMPORTS ||--o{ HEALTH_METRICS : "порождает"
    RAW_HEALTH_IMPORTS ||--o{ SYNC_LOGS : "логируется"

    EXERCISES ||--o{ CALIBRATION_RECORDS : "калибруется"
    EXERCISES ||--o{ QUEST_TEMPLATES : "шаблоны"
    QUEST_TEMPLATES ||--o{ DAILY_QUESTS : "генерирует"
    DAILY_QUESTS ||--o| QUEST_COMPLETIONS : "выполнение"

    ACHIEVEMENTS ||--o{ USER_ACHIEVEMENTS : "получено"
    ITEMS ||--o{ LOOTBOX_REWARDS : "награда лутбокса"
    ITEMS ||--o{ USER_INVENTORY : "в инвентаре"
    ITEMS ||--o{ BOSSES : "награда босса"
    ITEMS ||--o{ ACHIEVEMENTS : "награда достижения"
    LOOTBOXES ||--o{ LOOTBOX_REWARDS : "содержит"
```

## Схемы таблиц

### Аккаунты

```mermaid
erDiagram
    USERS {
        int    id PK
        string username UK
        string password_hash
        int    level
        int    experience
        int    strength
        int    endurance
        int    core
        int    recovery
        datetime created_at
        datetime updated_at
    }
    PROFILES {
        int    id PK
        int    user_id FK
        string display_name
        date   birth_date
        float  height_cm
        string goal_notes
        datetime created_at
    }
```

### HealthSync

```mermaid
erDiagram
    METRIC_DEFINITIONS {
        int    id PK
        enum   metric_type UK
        string name
        string base_unit
        string description
        bool   is_active
        datetime created_at
    }
    RAW_HEALTH_IMPORTS {
        int      id PK
        int      user_id FK
        string   source
        string   file_name
        string   file_hash
        string   format
        text     raw_data
        datetime imported_at
        enum     status
    }
    HEALTH_METRICS {
        int      id PK
        int      user_id FK
        int      import_id FK
        datetime timestamp
        enum     metric_type
        float    value
        string   unit
        string   source
        json     raw_data
        datetime created_at
    }
    SYNC_LOGS {
        int      id PK
        int      user_id FK
        int      import_id FK
        enum     level
        string   message
        json     details
        datetime created_at
    }
```

### Упражнения и калибровка

```mermaid
erDiagram
    EXERCISES {
        int    id PK
        string name UK
        enum   category
        enum   measurement_type
        string unit
        string description
        bool   is_custom
        int    created_by FK
        datetime created_at
    }
    CALIBRATION_RECORDS {
        int      id PK
        int      user_id FK
        int      exercise_id FK
        float    value
        string   unit
        datetime performed_at
        string   notes
    }
```

### Квесты

```mermaid
erDiagram
    QUEST_TEMPLATES {
        int    id PK
        int    exercise_id FK
        string name
        string description
        enum   category
        float  base_value
        string unit
        int    base_exp
        float  difficulty
        bool   is_active
        datetime created_at
    }
    DAILY_QUESTS {
        int      id PK
        int      user_id FK
        int      template_id FK
        date     date
        string   name
        string   description
        enum     category
        float    target_value
        string   unit
        int      exp_reward
        float    difficulty
        enum     status
        datetime completed_at
        datetime created_at
    }
    QUEST_COMPLETIONS {
        int    id PK
        int    user_id FK
        int    quest_id FK
        date   date
        float  planned_value
        float  actual_value
        int    exp_earned
        float  modifier
        enum   source
        datetime created_at
    }
```

### Готовность

```mermaid
erDiagram
    READINESS_SCORES {
        int      id PK
        int      user_id FK
        date     date
        int      score
        float    training_modifier
        string   reason
        datetime created_at
    }
```

### Игра

```mermaid
erDiagram
    BOSSES {
        int      id PK
        int      user_id FK
        string   name
        string   description
        enum     target_type
        float    target_value
        float    current_value
        bool     is_defeated
        datetime defeated_at
        int      reward_id FK
        datetime created_at
    }
    ACHIEVEMENTS {
        int    id PK
        string code UK
        string name
        string description
        json   condition
        int    reward_id FK
        datetime created_at
    }
    USER_ACHIEVEMENTS {
        int      id PK
        int      user_id FK
        int      achievement_id FK
        datetime unlocked_at
    }
    ITEMS {
        int    id PK
        string name UK
        string description
        enum   item_type
        datetime created_at
    }
    LOOTBOXES {
        int    id PK
        string name
        string description
        datetime created_at
    }
    LOOTBOX_REWARDS {
        int    id PK
        int    lootbox_id FK
        int    item_id FK
        float  probability
    }
    USER_INVENTORY {
        int      id PK
        int      user_id FK
        int      item_id FK
        int      quantity
        datetime acquired_at
    }
```

## Инвентарь таблиц

| # | Таблица               | Спринт | Назначение                              |
|---|-----------------------|--------|-----------------------------------------|
| 1 | `users`               | 1      | Аккаунт + игровые характеристики        |
| 2 | `profiles`            | 1      | Персональные данные (1:1 к users)       |
| 3 | `metric_definitions`  | 3      | Справочник метрик и единиц              |
| 4 | `raw_health_imports`  | 3      | Неизменяемые исходные импорты           |
| 5 | `health_metrics`      | 3      | Нормализованные метрики                 |
| 6 | `sync_logs`           | 3      | Логи синхронизации                      |
| 7 | `exercises`           | 2      | Упражнения (встроенные и custom)        |
| 8 | `calibration_records` | 2      | Результаты калибровочных тестов         |
| 9 | `quest_templates`     | 5      | Шаблоны заданий                         |
| 10| `daily_quests`        | 5      | Сгенерированные квесты на день          |
| 11| `quest_completions`   | 5      | Факты выполнения квестов                |
| 12| `readiness_scores`    | 4      | Оценки готовности                       |
| 13| `bosses`              | 6      | Долгосрочные цели                       |
| 14| `achievements`        | 6      | Достижения (определения)                |
| 15| `user_achievements`   | 6      | Полученные достижения                   |
| 16| `items`               | 6      | Игровые предметы/награды                |
| 17| `lootboxes`           | 6      | Лутбоксы                                |
| 18| `lootbox_rewards`     | 6      | Содержимое лутбоксов                    |
| 19| `user_inventory`      | 6      | Инвентарь пользователя                  |

## Ключевые ограничения целостности

- `raw_health_imports`: `UNIQUE(user_id, file_hash)` — идемпотентность импорта.
- `readiness_scores`: `UNIQUE(user_id, date)` — одна оценка в день.
- `daily_quests`: `UNIQUE(user_id, date, template_id)` — без дублей квестов.
- `user_achievements`: `UNIQUE(user_id, achievement_id)` — без дублей наград.
- `user_inventory`: `UNIQUE(user_id, item_id)` — стекинг предметов.
- `health_metrics`: индексы `(user_id, timestamp)`, `(user_id, metric_type, timestamp)`, `(metric_type)`, `(import_id)`.