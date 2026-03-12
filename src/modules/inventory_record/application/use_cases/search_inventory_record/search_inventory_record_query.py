from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class SearchInventoryRecordQuery:
    product_id: str
    start_timestamp: datetime | None = None
    end_timestamp: datetime | None = None
    limit: int = 20
    offset: int = 0
