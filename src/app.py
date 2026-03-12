from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.common.exceptions import AppException
from src.common.response import ApiResponse
from src.container import Container
from src.modules.inventory_record.presentation import router as inventory_record_router
from src.modules.shared.health import router as health_router


class App:

    def __init__(self) -> None:
        self._container = Container()
        self._fastapi = FastAPI(lifespan=self._lifespan)
        self._register_routes()
        self._register_exception_handlers()

    @asynccontextmanager
    async def _lifespan(self, _app: FastAPI) -> AsyncIterator[None]:
        env = self._container.config.env()
        await env.load()

        secrets = self._container.config.secrets()
        await secrets.load()

        db = self._container.database.db()
        await db.start_sessions()

        secrets.subscribe("db", lambda _k, v: db.restart_sessions(v))

        yield

    def _register_routes(self) -> None:
        self._fastapi.include_router(health_router)
        self._fastapi.include_router(inventory_record_router)

    def _register_exception_handlers(self) -> None:
        @self._fastapi.exception_handler(AppException)
        async def handle_app_exception(_request: Request, exc: AppException) -> JSONResponse:
            return JSONResponse(
                status_code=exc.exception_type,
                content=ApiResponse.fail(
                    error=exc.code,
                    message=exc.message,
                ).model_dump(),
            )

    @property
    def fastapi(self) -> FastAPI:
        return self._fastapi
