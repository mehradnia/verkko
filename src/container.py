from __future__ import annotations

from dependency_injector import containers, providers

from src.modules.inventory_record.container import InventoryContainer
from src.modules.shared.config.container import ConfigContainer
from src.modules.shared.database.container import DatabaseContainer


class Container(containers.DeclarativeContainer):

    config = providers.Container(ConfigContainer)

    database = providers.Container(
        DatabaseContainer,
        config=config,
    )

    inventory = providers.Container(
        InventoryContainer,
        database=database,
    )
