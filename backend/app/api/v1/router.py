"""API-роутеры Ascend (версия v1).

Маршруты подключаются по мере реализации спринтов согласно API-контракту
(см. docs/api-contract.md).
"""

from fastapi import APIRouter

from app.api.v1.calibration import router as calibration_router
from app.api.v1.exercises import router as exercises_router
from app.api.v1.profile import router as profile_router
from app.api.v1.users import router as users_router

api_router = APIRouter()

# Sprint 1
api_router.include_router(users_router)
api_router.include_router(profile_router)
api_router.include_router(calibration_router)
api_router.include_router(exercises_router)


@api_router.get("/health", tags=["system"])
def healthcheck() -> dict:
    """Проверка работоспособности API."""
    return {"status": "ok"}
