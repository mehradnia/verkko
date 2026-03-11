from __future__ import annotations

import os

from pydantic import BaseModel

from src.modules.shared.config.application.ports.config_manager import ConfigManager


class EnvManager(ConfigManager):

    def __init__(self, keys: list[str], schema: type[BaseModel] | None = None) -> None:
        super().__init__(schema)
        self._keys = keys

    async def _fetch(self) -> None:
        for key in self._keys:
            value = os.environ.get(key)
            if value is not None:
                self._config[key] = value
