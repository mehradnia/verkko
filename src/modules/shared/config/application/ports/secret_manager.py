from __future__ import annotations

import asyncio
from abc import abstractmethod
from typing import Any

from src.common.logger import Logger
from src.modules.shared.config.application.ports.config_manager import ConfigManager

logger = Logger.get_instance(__name__)


class SecretManager(ConfigManager):

    def __init__(self, refresh_ratio: float = 0.8, max_retries: int = 5) -> None:
        super().__init__()
        self._refresh_ratio = refresh_ratio
        self._max_retries = max_retries

    async def load(self) -> None:
        secrets = await self._fetch_all()
        for key, value, refresh_in in secrets:
            self._config[key] = value
            asyncio.create_task(self._rotate(key, refresh_in))

    @abstractmethod
    async def _fetch_all(self) -> list[tuple[str, Any, int]]:
        """Fetch all secrets. Returns list of (key, value, refresh_interval_seconds)."""
        ...

    @abstractmethod
    async def _fetch_one(self, key: str) -> tuple[Any, int]:
        """Fetch a single secret by key. Returns (value, refresh_interval_seconds)."""
        ...

    async def _rotate(self, key: str, refresh_in: int) -> None:
        retries = 0
        while True:
            await asyncio.sleep(refresh_in * self._refresh_ratio)
            try:
                value, refresh_in = await self._fetch_one(key)
                self._config[key] = value
                retries = 0
            except Exception:
                retries += 1
                if retries >= self._max_retries:
                    logger.critical(f"Secret rotation failed for '{key}' after {self._max_retries} retries")
                    raise
                logger.warning(f"Secret rotation failed for '{key}', retry {retries}/{self._max_retries}")
                await asyncio.sleep(min(refresh_in * 0.1, 30))
