from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.common.response import ApiResponse
from src.modules.inventory_record.application.use_cases.create_inventory_records.create_inventory_records_command import (
    CreateInventoryRecordItem,
    CreateInventoryRecordsCommand,
)
from src.modules.inventory_record.application.use_cases.create_inventory_records.create_inventory_records_use_case import (
    CreateInventoryRecordsUseCase,
)
from src.modules.inventory_record.container import InventoryContainer
from src.modules.inventory_record.presentation.dtos import (
    CreateInventoryRecordsRequestDto,
    CreateInventoryRecordsResponseDto,
    InventoryRecordResponseDto,
)

router = APIRouter(prefix="/inventory", tags=["Inventory"])


@router.post("/update")
@inject
async def create_inventory_records(
    body: CreateInventoryRecordsRequestDto,
    use_case: CreateInventoryRecordsUseCase = Depends(
        Provide[InventoryContainer.create_use_case]
    ),
):
    command = CreateInventoryRecordsCommand(
        items=[
            CreateInventoryRecordItem(
                product_id=item.productid,
                quantity=item.quantity,
                timestamp=item.timestamp,
            )
            for item in body.items
        ]
    )

    result = await use_case.execute(command)

    return ApiResponse.ok(
        data=CreateInventoryRecordsResponseDto(
            records=[
                InventoryRecordResponseDto(
                    id=record.id,
                    productid=record.product_id,
                    quantity=record.quantity,
                    timestamp=record.timestamp,
                )
                for record in result.records
            ],
            count=result.count,
        )
    )
