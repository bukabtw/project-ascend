"""Утилиты безопасности Ascend (раздел 56 ТЗ).

Хэширование паролей через bcrypt, проверка учётных данных.
"""

from __future__ import annotations

import bcrypt


def hash_password(password: str) -> str:
    """Возвращает bcrypt-хэш пароля."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    """Проверяет, соответствует ли пароль сохранённому хэшу."""
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except (ValueError, TypeError):
        return False
