from sqlalchemy import insert, select

from src.common.logger import Logger
from src.modules.inventory_record.application.ports.inventory_repository import InventoryRepository
from src.modules.inventory_record.domain.entities.inventory_record import InventoryRecord
from src.modules.inventory_record.infrastructure.entities.inventory_record_sqlalchemy import (
    InventoryRecordSqlAlchemy,
)
from src.modules.shared.database.infrastructure.adapters.sqlalchemy_adapter import SqlAlchemyAdapter


class SqlAlchemyInventoryRepository(InventoryRepository):

    _logger = Logger.get_instance(__name__)

    def __init__(self, db: SqlAlchemyAdapter) -> None:
        self._db = db

    async def save_many(self, records: list[InventoryRecord]) -> list[InventoryRecord]:
        async with self._db.get_session() as session:
            orm_records = [
                InventoryRecordSqlAlchemy(
                    product_id=record.product_id,
                    quantity=record.quantity,
                    timestamp=record.timestamp,
                )
                for record in records
            ]

            session.add_all(orm_records)
            await session.flush()

            return [
                InventoryRecord(
                    id=orm.id,
                    product_id=orm.product_id,
                    quantity=orm.quantity,
                    timestamp=orm.timestamp,
                )
                for orm in orm_records
            ]
