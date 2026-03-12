from src.common.dtos import PaginatedResponseDto
from src.modules.inventory_record.presentation.dtos.inventory_record_response_dto import (
    InventoryRecordResponseDto,
)


class SearchInventoryRecordsResponseDto(PaginatedResponseDto[InventoryRecordResponseDto]):
    pass
