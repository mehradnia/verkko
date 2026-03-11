from __future__ import annotations

from typing import Any

import httpx

from src.modules.shared.config.application.ports.secret_manager import SecretManager


class VaultPaths:
    DATABASE_CREDS = "/v1/database/creds"


class VaultSecretManager(SecretManager):

    def __init__(self, addr: str, token: str, roles: dict[str, str]) -> None:
        super().__init__()
        self._roles = roles
        self._client = httpx.AsyncClient(
            base_url=addr.rstrip("/"),
            headers={"X-Vault-Token": token},
        )

    async def _fetch_all(self) -> list[tuple[str, Any, int]]:
        results = []
        for key in self._roles:
            value, refresh_in = await self._fetch_one(key)
            results.append((key, value, refresh_in))
        return results

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
