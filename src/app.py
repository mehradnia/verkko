from __future__ import annotations

from fastapi import FastAPI

from src.modules.shared.health import router as health_router


def create_app() -> FastAPI:
    application = FastAPI()

    application.include_router(health_router)

    return application
