from collections.abc import Callable
from typing import Any

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute

from src.common.response import ApiResponse


class ApiRoute(APIRoute):

    def get_route_handler(self) -> Callable:
        original_handler = super().get_route_handler()

        async def wrapped_handler(request: Request) -> Response:
            response = await original_handler(request)

            if isinstance(response, JSONResponse):
                return response

            body = response.body
            if isinstance(body, bytes):
                import json
                body = json.loads(body)

            wrapped = ApiResponse.ok(data=body)
            return JSONResponse(
                status_code=response.status_code,
                content=wrapped.model_dump(),
            )

        return wrapped_handler
