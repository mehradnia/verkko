from dataclasses import dataclass

from src.modules.inventory_record.application.use_cases.create_inventory_records.create_inventory_records_result import (
    InventoryRecordItem,
)


@dataclass(frozen=True)
class SearchInventoryRecordResult:
    items: list[InventoryRecordItem]
    total: int
