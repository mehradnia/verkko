from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

from src.common.logger import Logger


class ConfigManager(ABC):

    _logger = Logger.get_instance(__name__)

    def __init__(self) -> None:
        self._config: dict[str, Any] = {}
        self._subscribers: dict[str, list[Callable[[str, Any], None]]] = {}

    def get(self, key: str) -> Any:
        return self._config.get(key)

    def subscribe(self, key: str, callback: Callable[[str, Any], None]) -> None:
        if key not in self._subscribers:
            self._subscribers[key] = []
        self._subscribers[key].append(callback)

    def _notify(self, key: str, value: Any) -> None:
        for callback in self._subscribers.get(key, []):
            try:
                callback(key, value)
            except Exception:
                self._logger.error(f"Listener failed for key '{key}'")

    @abstractmethod
    async def load(self) -> None: ...
