from abc import ABC, abstractmethod

from src.modules.inventory_record.domain.entities.inventory_record import InventoryRecord


class InventoryRepository(ABC):

    @abstractmethod
    async def save_many(self, records: list[InventoryRecord]) -> list[InventoryRecord]: ...
