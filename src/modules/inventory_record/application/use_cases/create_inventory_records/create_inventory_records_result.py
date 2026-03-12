from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class CreatedInventoryRecordItem:
    id: int
    product_id: str
    quantity: int
    timestamp: datetime


@dataclass(frozen=True)
class CreateInventoryRecordsResult:
    records: list[CreatedInventoryRecordItem]
    count: int
