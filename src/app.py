from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.common.filters import ExceptionFilter
from src.container import Container
from src.routes import register_routes


class App:

    def __init__(self) -> None:
        self._container = Container()
        self._fastapi = FastAPI(lifespan=self._lifespan)
        ExceptionFilter(self._fastapi)

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

    @property
    def fastapi(self) -> FastAPI:
        return self._fastapi
