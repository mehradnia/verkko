from __future__ import annotations

import asyncio
from typing import Any

import httpx

from src.modules.shared.config.application.ports.config_manager import ConfigManager


class VaultPaths:
    DATABASE_CREDS = "/v1/database/creds"


class VaultSecretManager(ConfigManager):

    def __init__(
        self,
        addr: str,
        token: str,
        roles: dict[str, str],
        refresh_ratio: float = 0.8,
        max_retries: int = 5,
    ) -> None:
        super().__init__()
        self._roles = roles
        self._refresh_ratio = refresh_ratio
        self._max_retries = max_retries
        self._client = httpx.AsyncClient(
            base_url=addr.rstrip("/"),
            headers={"X-Vault-Token": token},
        )

    async def _fetch(self) -> None:
        for key in self._roles:
            credentials, refresh_in = await self._fetch_one(key)
            self._config[key] = credentials
            asyncio.create_task(self._rotate(key, refresh_in))

    async def _fetch_one(self, key: str) -> tuple[Any, int]:
        role = self._roles[key]
        response = await self._client.get(f"{VaultPaths.DATABASE_CREDS}/{role}")
        response.raise_for_status()
        data = response.json()
        credentials = {
            "username": data["data"]["username"],
            "password": data["data"]["password"],
        }
        return credentials, data["lease_duration"]

    async def _rotate(self, key: str, refresh_in: int) -> None:
        retries = 0
        while True:
            await asyncio.sleep(refresh_in * self._refresh_ratio)
            try:
                value, refresh_in = await self._fetch_one(key)
                self._config[key] = value
                self._notify(key, value)
                retries = 0
            except Exception:
                retries += 1
                if retries >= self._max_retries:
                    self._logger.critical(f"Secret rotation failed for '{key}' after {self._max_retries} retries")
                    raise
                self._logger.warning(f"Secret rotation failed for '{key}', retry {retries}/{self._max_retries}")
                await asyncio.sleep(min(refresh_in * 0.1, 30))
