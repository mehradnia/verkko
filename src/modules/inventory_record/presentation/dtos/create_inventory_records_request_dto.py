from datetime import datetime

from pydantic import BaseModel, Field


class InventoryRecordItemDto(BaseModel):
    productid: str = Field(min_length=1)
    quantity: int = Field(ge=0)
    timestamp: datetime


class CreateInventoryRecordsRequestDto(BaseModel):
    items: list[InventoryRecordItemDto] = Field(min_length=1)
