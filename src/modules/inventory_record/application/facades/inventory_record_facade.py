from abc import ABC, abstractmethod

from src.modules.inventory_record.application.use_cases.create_inventory_records.create_inventory_records_command import (
    CreateInventoryRecordsCommand,
)
from src.modules.inventory_record.application.use_cases.create_inventory_records.create_inventory_records_result import (
    CreateInventoryRecordsResult,
)
from src.modules.inventory_record.application.use_cases.search_inventory_record.search_inventory_record_query import (
    SearchInventoryRecordQuery,
)
from src.modules.inventory_record.application.use_cases.search_inventory_record.search_inventory_record_result import (
    SearchInventoryRecordResult,
)


class InventoryRecordFacade(ABC):

    @abstractmethod
    async def create_inventory_records(
        self, command: CreateInventoryRecordsCommand,
    ) -> CreateInventoryRecordsResult: ...

    @abstractmethod
    async def search_inventory_records(
        self, query: SearchInventoryRecordQuery,
    ) -> SearchInventoryRecordResult: ...
