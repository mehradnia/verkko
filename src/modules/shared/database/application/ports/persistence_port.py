from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from typing import Any


class PersistencePort(ABC):

    @abstractmethod
    async def start_sessions(self) -> None: ...

    @abstractmethod
    def restart_sessions(self, credentials: Any) -> None: ...

    @abstractmethod
    def get_session(self) -> AsyncIterator[Any]: ...
