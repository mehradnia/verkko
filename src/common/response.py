from datetime import datetime, timezone
from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool
    data: T | None = None
    message: str | None = None
    error: str | None = None
    timestamp: str

    @staticmethod
    def ok(data: Any = None, message: str | None = None) -> "ApiResponse":
        return ApiResponse(
            success=True,
            data=data,
            message=message,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

    @staticmethod
    def fail(error: str, message: str | None = None) -> "ApiResponse":
        return ApiResponse(
            success=False,
            error=error,
            message=message,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
