from abc import ABC, abstractmethod

from src.modules.inventory_record.application.use_cases.create_inventory_records.create_inventory_records_command import (
    CreateInventoryRecordsCommand,
)
from src.modules.inventory_record.application.use_cases.create_inventory_records.create_inventory_records_result import (
    CreateInventoryRecordsResult,
)


class InventoryRecordFacade(ABC):

    @abstractmethod
    async def create_inventory_records(
        self, command: CreateInventoryRecordsCommand,
    ) -> CreateInventoryRecordsResult: ...
