from __future__ import annotations

from dependency_injector import containers, providers

from src.modules.shared.database.infrastructure.adapters.sqlalchemy_adapter import SqlAlchemyAdapter


class DatabaseContainer(containers.DeclarativeContainer):

    config = providers.DependenciesContainer()

    db = providers.Singleton(
        SqlAlchemyAdapter,
        host=providers.Callable(lambda c: c.get("DB_HOST") or "localhost", config.env),
        port=providers.Callable(lambda c: int(c.get("DB_PORT") or 5432), config.env),
        name=providers.Callable(lambda c: c.get("DB_NAME") or "verkko_db", config.env),
        credentials=providers.Callable(lambda c: c.get("db"), config.secrets),
        ssl=providers.Callable(lambda c: c.get("DB_SSL") != "false", config.env),
    )
