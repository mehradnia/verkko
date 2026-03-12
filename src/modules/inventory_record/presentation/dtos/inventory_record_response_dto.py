from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class InventoryRecordResponseDto(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    productid: str = Field(alias="product_id")
    quantity: int
    timestamp: datetime
