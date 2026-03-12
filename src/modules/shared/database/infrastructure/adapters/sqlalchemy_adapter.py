from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.common.logger import Logger
from src.modules.shared.database.application.ports.persistence_port import PersistencePort


class SqlAlchemyAdapter(PersistencePort):

    _logger = Logger.get_instance(__name__)

    def __init__(self, host: str, port: int, name: str, credentials: dict[str, str],
                 ssl: bool = True, sync: bool = False, entities: list[type[DeclarativeBase]] | None = None) -> None:
        self._host = host
        self._port = port
        self._name = name
        self._ssl = ssl
        self._sync = sync
        self._entities = entities or []
        self._engine: AsyncEngine | None = None
        self._session_factory: async_sessionmaker[AsyncSession] | None = None
        self._credentials = credentials

    async def start_sessions(self) -> None:
        self._build_engine(self._credentials)
        self._logger.info("Database connection established")

        # Dev-only: auto-sync ORM entities to DB schema (controlled by DB_SYNC env).
        # In production, use Alembic versioned migrations instead.
        if self._sync:
            async with self._engine.begin() as conn:
                for base in self._entities:
                    await conn.run_sync(base.metadata.create_all)
            self._logger.info("Database tables synced from ORM entities")

    def restart_sessions(self, credentials: Any) -> None:
        if self._engine is not None:
            asyncio.create_task(self._engine.dispose())
        self._build_engine(credentials)
        self._logger.info("Database credentials rotated, connection pool restarted")

    def _build_engine(self, credentials: dict[str, str]) -> None:
        ssl_param = "?ssl=require" if self._ssl else ""
        url = (
            f"postgresql+asyncpg://{credentials['username']}:{credentials['password']}"
            f"@{self._host}:{self._port}/{self._name}{ssl_param}"
        )
        self._engine = create_async_engine(url, pool_size=10, max_overflow=5)
        self._session_factory = async_sessionmaker(self._engine, expire_on_commit=False)

    @asynccontextmanager
    async def get_session(self) -> AsyncIterator[AsyncSession]:
        if self._session_factory is None:
            raise RuntimeError("Database not started. Call start_sessions() first.")
        async with self._session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
