from pydantic import BaseModel, ConfigDict

from src.modules.inventory_record.presentation.dtos.inventory_record_response_dto import (
    InventoryRecordResponseDto,
)


class CreateInventoryRecordsResponseDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    records: list[InventoryRecordResponseDto]
    count: int
