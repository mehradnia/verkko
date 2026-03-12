from datetime import datetime

from fastapi import APIRouter, Query

from src.common.interceptors import PresentationResponseHandler
from src.modules.inventory_record.application import (
    CreateInventoryRecordItem,
    CreateInventoryRecordsCommand,
    InventoryRecordFacade,
    SearchInventoryRecordQuery,
)
from src.modules.inventory_record.presentation.dtos import (
    CreateInventoryRecordsRequestDto,
    CreateInventoryRecordsResponseDto,
    SearchInventoryRecordsResponseDto,
)


class InventoryRecordController:

    def __init__(self, service: InventoryRecordFacade) -> None:
        self._service = service
        self._router = APIRouter(prefix="/inventory", tags=["Inventory"], route_class=PresentationResponseHandler)
        self._register_routes()

    @property
    def router(self) -> APIRouter:
        return self._router

    def _register_routes(self) -> None:
        self._router.post("/update")(self.create_inventory_records)
        self._router.get("/query")(self.search_inventory_records)

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

        return CreateInventoryRecordsResponseDto.model_validate(result, from_attributes=True)

    async def search_inventory_records(
        self,
        productid: str = Query(min_length=1),
        starttimestamp: datetime | None = Query(default=None),
        endtimestamp: datetime | None = Query(default=None),
        limit: int = Query(default=20, ge=1, le=100),
        offset: int = Query(default=0, ge=0),
    ):
        query = SearchInventoryRecordQuery(
            product_id=productid,
            start_timestamp=starttimestamp,
            end_timestamp=endtimestamp,
            limit=limit,
            offset=offset,
        )

        result = await self._service.search_inventory_records(query)

        return SearchInventoryRecordsResponseDto.model_validate(result, from_attributes=True)
