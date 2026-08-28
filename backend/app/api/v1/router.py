"""API-роутеры Ascend (версия v1).

Маршруты будут подключены в следующих спринтах согласно API-контракту
(см. docs/api-contract.md): Profile, Calibration, Health, Quests, Game,
Bosses, Achievements, Export.
"""

from fastapi import APIRouter

api_router = APIRouter()


@api_router.get("/health", tags=["system"])
def healthcheck() -> dict:
    """Проверка работоспособности API."""
    return {"status": "ok"}
