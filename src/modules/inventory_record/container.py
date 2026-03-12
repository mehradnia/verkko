from __future__ import annotations

from dependency_injector import containers, providers

from src.modules.inventory_record.application.services.inventory_record_application_service import (
    InventoryRecordApplicationService,
)
from src.modules.inventory_record.application.use_cases.create_inventory_records.create_inventory_records_use_case import (
    CreateInventoryRecordsUseCase,
)
from src.modules.inventory_record.application.use_cases.search_inventory_record.search_inventory_record_use_case import (
    SearchInventoryRecordUseCase,
)
from src.modules.inventory_record.infrastructure.adapters.sqlalchemy_inventory_repository import (
    SqlAlchemyInventoryRepository,
)
from src.modules.inventory_record.presentation.controllers.inventory_record_controller import (
    InventoryRecordController,
)


class InventoryContainer(containers.DeclarativeContainer):

    database = providers.DependenciesContainer()

    repository = providers.Singleton(
        SqlAlchemyInventoryRepository,
        db=database.db,
    )

    create_use_case = providers.Factory(
        CreateInventoryRecordsUseCase,
        repository=repository,
    )

    search_use_case = providers.Factory(
        SearchInventoryRecordUseCase,
        repository=repository,
    )

    application_service = providers.Factory(
        InventoryRecordApplicationService,
        create_inventory_records_use_case=create_use_case,
        search_inventory_record_use_case=search_use_case,
    )

    controller = providers.Singleton(
        InventoryRecordController,
        service=application_service,
    )
