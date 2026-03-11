from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class ConfigManager(ABC):

    def __init__(self) -> None:
        self._config: dict[str, Any] = {}

    def get(self, key: str) -> Any:
        return self._config.get(key)

    @abstractmethod
    async def load(self) -> None: ...
