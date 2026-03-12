from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.common.dtos import PresentationResponse
from src.common.exceptions import AppException


class ExceptionFilter:

    def __init__(self, app: FastAPI) -> None:
        self._app = app
        self._register()

    def _register(self) -> None:
        self._app.exception_handler(AppException)(self._handle_app_exception)
        self._app.exception_handler(RequestValidationError)(self._handle_validation_error)

    @staticmethod
    async def _handle_app_exception(_request: Request, exc: AppException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.exception_type,
            content=PresentationResponse.fail(
                error=exc.code,
                message=exc.message,
            ).model_dump(),
        )

    @staticmethod
    async def _handle_validation_error(_request: Request, exc: RequestValidationError) -> JSONResponse:
        errors = exc.errors()
        messages = [
            f"{' -> '.join(str(loc) for loc in e['loc'])}: {e['msg']}"
            for e in errors
        ]
        return JSONResponse(
            status_code=400,
            content=PresentationResponse.fail(
                error="VALIDATION_ERROR",
                message="; ".join(messages),
            ).model_dump(),
        )
