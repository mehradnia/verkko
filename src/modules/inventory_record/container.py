from __future__ import annotations

from dependency_injector import containers, providers

from src.modules.inventory_record.application.use_cases.create_inventory_records.create_inventory_records_use_case import (
    CreateInventoryRecordsUseCase,
)
from src.modules.inventory_record.infrastructure.adapters.sqlalchemy_inventory_repository import (
    SqlAlchemyInventoryRepository,
)


class InventoryContainer(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.modules.inventory_record.presentation.inventory_record_controller",
        ]
    )

    database = providers.DependenciesContainer()

    repository = providers.Singleton(
        SqlAlchemyInventoryRepository,
        db=database.db,
    )

    create_use_case = providers.Factory(
        CreateInventoryRecordsUseCase,
        repository=repository,
    )
