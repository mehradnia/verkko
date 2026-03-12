from datetime import datetime

from sqlalchemy import func, select

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

    async def search(
        self,
        product_id: str,
        start_timestamp: datetime | None = None,
        end_timestamp: datetime | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[InventoryRecord], int]:
        async with self._db.get_session() as session:
            conditions = [InventoryRecordSqlAlchemy.product_id == product_id]

            if start_timestamp is not None:
                conditions.append(InventoryRecordSqlAlchemy.timestamp >= start_timestamp)

            if end_timestamp is not None:
                conditions.append(InventoryRecordSqlAlchemy.timestamp <= end_timestamp)

            count_query = select(func.count()).select_from(InventoryRecordSqlAlchemy).where(*conditions)
            total = (await session.execute(count_query)).scalar_one()

            data_query = (
                select(InventoryRecordSqlAlchemy)
                .where(*conditions)
                .order_by(InventoryRecordSqlAlchemy.timestamp.asc())
                .limit(limit)
                .offset(offset)
            )

            result = await session.execute(data_query)
            rows = result.scalars().all()

            return [
                InventoryRecord(
                    id=row.id,
                    product_id=row.product_id,
                    quantity=row.quantity,
                    timestamp=row.timestamp,
                )
                for row in rows
            ], total
