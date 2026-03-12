from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CreateInventoryRecordItem:
    product_id: str
    quantity: int
    timestamp: datetime


@dataclass(frozen=True)
class CreateInventoryRecordsCommand:
    items: list[CreateInventoryRecordItem]
