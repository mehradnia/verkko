import json
from collections.abc import Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute

from src.common.response import ApiResponse


class ApiRoute(APIRoute):

    def get_route_handler(self) -> Callable:
        original_handler = super().get_route_handler()

        async def wrapped_handler(request: Request) -> Response:
            response = await original_handler(request)

            body = json.loads(response.body)

            if isinstance(body, dict) and "success" in body:
                return response

            wrapped = ApiResponse.ok(data=body)
            return JSONResponse(
                status_code=response.status_code,
                content=wrapped.model_dump(),
            )

        return wrapped_handler
