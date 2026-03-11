from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

from pydantic import BaseModel, ValidationError

from src.common.logger import Logger


class ConfigManager(ABC):

    _logger = Logger.get_instance(__name__)

    def __init__(self, schema: type[BaseModel] | None = None) -> None:
        self._config: dict[str, Any] = {}
        self._subscribers: dict[str, list[Callable[[str, Any], None]]] = {}
        self._schema = schema

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

    async def load(self) -> None:
        await self._fetch()
        self._validate()

    @abstractmethod
    async def _fetch(self) -> None: ...

    def _validate(self) -> None:
        if self._schema is None:
            return
        try:
            self._schema(**self._config)
            self._logger.info("Configuration validated successfully")
        except ValidationError as e:
            self._logger.critical(f"Configuration validation failed: {e}")
            raise
