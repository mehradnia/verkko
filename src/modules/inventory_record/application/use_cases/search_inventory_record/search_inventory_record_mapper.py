from src.modules.inventory_record.application.use_cases.create_inventory_records.create_inventory_records_result import (
    InventoryRecordItem,
)
from src.modules.inventory_record.application.use_cases.search_inventory_record.search_inventory_record_result import (
    SearchInventoryRecordResult,
)
from src.modules.inventory_record.domain.entities.inventory_record import InventoryRecord


class SearchInventoryRecordMapper:

    @staticmethod
    def to_result(records: list[InventoryRecord], total: int) -> SearchInventoryRecordResult:
        return SearchInventoryRecordResult(
            items=[
                InventoryRecordItem(
                    id=record.id,
                    product_id=record.product_id,
                    quantity=record.quantity,
                    timestamp=record.timestamp,
                )
                for record in records
            ],
            total=total,
        )
