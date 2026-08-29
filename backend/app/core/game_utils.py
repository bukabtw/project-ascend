"""Игровые расчёты: EXP, уровни (разделы 28-29 ТЗ).

Формулы вынесены сюда, чтобы роутеры и сервисы могли переиспользовать.
Коэффициенты берутся из конфигурации (раздел 57 ТЗ).
"""

from __future__ import annotations

from app.core.config import get_settings

settings = get_settings()


def exp_to_next_level(level: int) -> int:
    """EXP, необходимый для перехода с текущего уровня на следующий.

    ``EXP_next = EXP_base * LEVEL_MULTIPLIER^(level - 1)``
    """
    return int(settings.exp_base * (settings.level_multiplier ** (level - 1)))


def exp_to_next_remaining(current_exp: int, level: int) -> int:
    """Сколько EXP осталось до следующего уровня."""
    # EXP накапливается с уровня 1: на каждом уровне нужно exp_to_next_level.
    # experience — суммарный накопленный EXP.
    # Для упрощения: experience — прогресс в пределах текущего уровня.
    return max(0, exp_to_next_level(level) - current_exp)


def check_level_up(user) -> dict | None:
    """Проверяет, достиг ли пользователь следующего уровня.

    ``user.experience`` трактуется как прогресс в пределах текущего уровня.
    При превышении порога уровень повышается, излишек переносится.

    Возвращает ``{"new_level": int}`` если уровень повысился, иначе ``None``.
    """
    leveled_up = False
    while user.experience >= exp_to_next_level(user.level):
        user.experience -= exp_to_next_level(user.level)
        user.level += 1
        leveled_up = True
    return {"new_level": user.level} if leveled_up else None
