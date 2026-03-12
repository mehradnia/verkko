from abc import ABC, abstractmethod
from logging import Logger
from typing import Generic, TypeVar

from src.common.logger import Logger as AppLogger

TCommand = TypeVar("TCommand")
TResult = TypeVar("TResult")


class BaseUseCase(ABC, Generic[TCommand, TResult]):

    _logger: Logger = AppLogger.get_instance(__name__)

    @abstractmethod
    async def _execute(self, command: TCommand) -> TResult: ...

    async def execute(self, command: TCommand) -> TResult:
        return await self._execute(command)
