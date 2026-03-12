from src.modules.inventory_record.application.use_cases.create_inventory_records.create_inventory_records_result import (
    CreatedInventoryRecordItem,
    CreateInventoryRecordsResult,
)
from src.modules.inventory_record.domain.entities.inventory_record import InventoryRecord


class CreateInventoryRecordsMapper:

    @staticmethod
    def to_result(records: list[InventoryRecord]) -> CreateInventoryRecordsResult:
        return CreateInventoryRecordsResult(
            records=[
                CreatedInventoryRecordItem(
                    id=record.id,
                    product_id=record.product_id,
                    quantity=record.quantity,
                    timestamp=record.timestamp,
                )
                for record in records
            ],
            count=len(records),
        )
