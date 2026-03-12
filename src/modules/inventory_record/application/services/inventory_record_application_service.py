from src.modules.inventory_record.application.facades.inventory_record_facade import (
    InventoryRecordFacade,
)
from src.modules.inventory_record.application.use_cases.create_inventory_records.create_inventory_records_command import (
    CreateInventoryRecordsCommand,
)
from src.modules.inventory_record.application.use_cases.create_inventory_records.create_inventory_records_result import (
    CreateInventoryRecordsResult,
)
from src.modules.inventory_record.application.use_cases.create_inventory_records.create_inventory_records_use_case import (
    CreateInventoryRecordsUseCase,
)


class InventoryRecordApplicationService(InventoryRecordFacade):

    def __init__(
        self,
        create_inventory_records_use_case: CreateInventoryRecordsUseCase,
    ) -> None:
        self._create_inventory_records_use_case = create_inventory_records_use_case

    async def create_inventory_records(
        self, command: CreateInventoryRecordsCommand,
    ) -> CreateInventoryRecordsResult:
        return await self._create_inventory_records_use_case.execute(command)
