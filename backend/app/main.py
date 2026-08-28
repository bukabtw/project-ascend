"""Точка входа backend-приложения Ascend (FastAPI)."""

from __future__ import annotations

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import get_settings

settings = get_settings()


def create_app() -> FastAPI:
    """Фабрика FastAPI-приложения."""
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        debug=settings.debug,
        openapi_url=f"{settings.api_prefix}/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.include_router(api_router, prefix=settings.api_prefix)

    @app.get("/", tags=["system"])
    def root() -> dict:
        return {
            "name": settings.app_name,
            "version": settings.app_version,
            "env": settings.app_env,
            "docs": "/docs",
        }

    return app


app = create_app()


def run() -> None:
    """Запуск локального сервера (точка входа console-script ``ascend-api``)."""
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=settings.debug,
    )
