from datetime import datetime

from pydantic import BaseModel


class InventoryRecordResponseDto(BaseModel):
    id: int
    productid: str
    quantity: int
    timestamp: datetime


class CreateInventoryRecordsResponseDto(BaseModel):
    records: list[InventoryRecordResponseDto]
    count: int
