from __future__ import annotations

from enum import IntEnum


class ExceptionType(IntEnum):
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    UNPROCESSABLE = 422
    INTERNAL = 500


class AppException(Exception):

    def __init__(self, message: str, code: str, exception_type: ExceptionType) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.exception_type = exception_type
