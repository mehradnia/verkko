from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.common.exceptions import AppException
from src.common.dtos import PresentationResponse
from src.container import Container
from src.routes import register_routes


class App:

    def __init__(self) -> None:
        self._container = Container()
        self._fastapi = FastAPI(lifespan=self._lifespan)
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

        self._register_routes()

        yield

    def _register_routes(self) -> None:
        register_routes(self._fastapi, self._container)

    def _register_exception_handlers(self) -> None:
        @self._fastapi.exception_handler(AppException)
        async def handle_app_exception(_request: Request, exc: AppException) -> JSONResponse:
            return JSONResponse(
                status_code=exc.exception_type,
                content=PresentationResponse.fail(
                    error=exc.code,
                    message=exc.message,
                ).model_dump(),
            )

        @self._fastapi.exception_handler(RequestValidationError)
        async def handle_validation_error(_request: Request, exc: RequestValidationError) -> JSONResponse:
            errors = exc.errors()
            messages = [
                f"{' -> '.join(str(loc) for loc in e['loc'])}: {e['msg']}"
                for e in errors
            ]
            return JSONResponse(
                status_code=400,
                content=PresentationResponse.fail(
                    error="VALIDATION_ERROR",
                    message="; ".join(messages),
                ).model_dump(),
            )

    @property
    def fastapi(self) -> FastAPI:
        return self._fastapi
