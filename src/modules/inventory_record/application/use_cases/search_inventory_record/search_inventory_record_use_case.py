from src.common.logger import Logger
from src.common.abstracts import BaseUseCase
from src.modules.inventory_record.application.ports.inventory_repository import InventoryRepository
from src.modules.inventory_record.application.use_cases.search_inventory_record.search_inventory_record_mapper import (
    SearchInventoryRecordMapper,
)
from src.modules.inventory_record.application.use_cases.search_inventory_record.search_inventory_record_query import (
    SearchInventoryRecordQuery,
)
from src.modules.inventory_record.application.use_cases.search_inventory_record.search_inventory_record_result import (
    SearchInventoryRecordResult,
)


class SearchInventoryRecordUseCase(BaseUseCase[SearchInventoryRecordQuery, SearchInventoryRecordResult]):

    _logger = Logger.get_instance(__name__)

    def __init__(self, repository: InventoryRepository) -> None:
        self._repository = repository

    async def _execute(self, query: SearchInventoryRecordQuery) -> SearchInventoryRecordResult:
        self._logger.info(f"Searching inventory records for product '{query.product_id}'")

        records, total = await self._repository.search(
            product_id=query.product_id,
            start_timestamp=query.start_timestamp,
            end_timestamp=query.end_timestamp,
            limit=query.limit,
            offset=query.offset,
        )

        self._logger.info(f"Found {len(records)} of {total} inventory records")

        return SearchInventoryRecordMapper.to_result(records, total)
