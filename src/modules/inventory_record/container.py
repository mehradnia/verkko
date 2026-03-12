from __future__ import annotations

from dependency_injector import containers, providers


class InventoryContainer(containers.DeclarativeContainer):

    database = providers.DependenciesContainer()
