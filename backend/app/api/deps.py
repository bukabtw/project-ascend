"""FastAPI-зависимости.

Аутентификация локального приложения через заголовок ``X-Ascend-User``
(раздел 56 ТЗ, docs/api-contract.md). Для локального режима этого достаточно:
приложение работает offline-first, пароли хранятся в виде хэша, но доступ
к API идентифицируется по ID пользователя.
"""

from __future__ import annotations

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User


def get_current_user(
    db: Session = Depends(get_db),
    x_ascend_user: str | None = Header(default=None, alias="X-Ascend-User"),
) -> User:
    """Возвращает текущего пользователя по заголовку ``X-Ascend-User``.

    Заголовок содержит числовой ID пользователя. Если пользователь не найден
    или заголовок отсутствует — 401/403.
    """
    if x_ascend_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-Ascend-User header",
        )

    try:
        user_id = int(x_ascend_user)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid X-Ascend-User header: expected integer user ID",
        ) from None

    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not found",
        )
    return user
