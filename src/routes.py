from fastapi import FastAPI

from src.container import Container
from src.modules.shared.health import router as health_router


def register_routes(app: FastAPI, container: Container) -> None:
    app.include_router(health_router)

    inventory_controller = container.inventory.controller()
    app.include_router(inventory_controller.router)
