from fastapi import APIRouter

from src.common.api_route import ApiRoute
from src.modules.inventory_record.application import (
    CreateInventoryRecordItem,
    CreateInventoryRecordsCommand,
    InventoryRecordFacade,
)
from src.modules.inventory_record.presentation.dtos import (
    CreateInventoryRecordsRequestDto,
    CreateInventoryRecordsResponseDto,
    InventoryRecordResponseDto,
)


class InventoryRecordController:

    def __init__(self, service: InventoryRecordFacade) -> None:
        self._service = service
        self._router = APIRouter(prefix="/inventory", tags=["Inventory"], route_class=ApiRoute)
        self._register_routes()

    @property
    def router(self) -> APIRouter:
        return self._router

    def _register_routes(self) -> None:
        self._router.post("/update")(self.create_inventory_records)

    async def create_inventory_records(
        self, body: CreateInventoryRecordsRequestDto,
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

        result = await self._service.create_inventory_records(command)

        return CreateInventoryRecordsResponseDto(
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
