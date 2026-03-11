from __future__ import annotations

import os

from src.modules.shared.config.application.ports.config_manager import ConfigManager


class EnvManager(ConfigManager):

    def __init__(self, keys: list[str]) -> None:
        super().__init__()
        self._keys = keys

    async def load(self) -> None:
        for key in self._keys:
            value = os.environ.get(key)
            if value is not None:
                self._config[key] = value
