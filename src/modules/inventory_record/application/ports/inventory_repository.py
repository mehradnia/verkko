from abc import ABC, abstractmethod
from datetime import datetime

from src.modules.inventory_record.domain.entities.inventory_record import InventoryRecord


class InventoryRepository(ABC):

    @abstractmethod
    async def save_many(self, records: list[InventoryRecord]) -> list[InventoryRecord]: ...

    @abstractmethod
    async def search(
        self,
        product_id: str,
        start_timestamp: datetime | None = None,
        end_timestamp: datetime | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[InventoryRecord], int]: ...
