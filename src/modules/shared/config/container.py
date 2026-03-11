from __future__ import annotations

from dependency_injector import containers, providers

from src.modules.shared.config.application.schemas.config_schema import ConfigSchema
from src.modules.shared.config.infrastructure.adapters.env_manager import EnvManager
from src.modules.shared.config.infrastructure.adapters.vault_secret_manager import VaultSecretManager


class ConfigContainer(containers.DeclarativeContainer):

    env = providers.Singleton(
        EnvManager,
        schema=ConfigSchema,
    )

    secrets = providers.Singleton(
        VaultSecretManager,
        addr=providers.Callable(lambda env: env.get("VAULT_ADDR"), env),
        token=providers.Callable(lambda env: env.get("VAULT_TOKEN"), env),
        roles={"db": "verkko-service"},
    )
