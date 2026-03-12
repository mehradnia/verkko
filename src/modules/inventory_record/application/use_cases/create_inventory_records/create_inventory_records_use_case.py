from src.common.logger import Logger
from src.common.use_case import BaseUseCase
from src.modules.inventory_record.application.ports.inventory_repository import InventoryRepository
from src.modules.inventory_record.application.use_cases.create_inventory_records.create_inventory_records_command import (
    CreateInventoryRecordsCommand,
)
from src.modules.inventory_record.application.use_cases.create_inventory_records.create_inventory_records_mapper import (
    CreateInventoryRecordsMapper,
)
from src.modules.inventory_record.application.use_cases.create_inventory_records.create_inventory_records_result import (
    CreateInventoryRecordsResult,
)
from src.modules.inventory_record.domain.entities.inventory_record import InventoryRecord


class CreateInventoryRecordsUseCase(BaseUseCase[CreateInventoryRecordsCommand, CreateInventoryRecordsResult]):

    _logger = Logger.get_instance(__name__)

    def __init__(self, repository: InventoryRepository) -> None:
        self._repository = repository

    async def _execute(self, command: CreateInventoryRecordsCommand) -> CreateInventoryRecordsResult:
        self._logger.info(f"Creating {len(command.items)} inventory records")

        records = [
            InventoryRecord(
                product_id=item.product_id,
                quantity=item.quantity,
                timestamp=item.timestamp,
            )
            for item in command.items
        ]
        saved = await self._repository.save_many(records)

        self._logger.info(f"Successfully created {len(saved)} inventory records")

        return CreateInventoryRecordsMapper.to_result(saved)
