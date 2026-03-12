from __future__ import annotations

from pydantic import BaseModel, Field


class ConfigSchema(BaseModel):
    SERVICE_NAME: str
    SERVICE_VERSION: str
    SERVICE_ENV: str
    SERVICE_DEBUG: str = "false"
    SERVICE_HOST: str = "0.0.0.0"
    SERVICE_PORT: int = Field(default=8080, ge=1, le=65535)
    SERVICE_LOG_LEVEL: str = "INFO"
    SERVICE_CORS_ORIGINS: str = "*"
    VAULT_ADDR: str
    VAULT_TOKEN: str
    DB_HOST: str
    DB_PORT: int = Field(default=5432, ge=1, le=65535)
    DB_NAME: str
    DB_SSL: str = "true"
    DB_SYNC: str = "false"
