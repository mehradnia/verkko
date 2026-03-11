from datetime import datetime

from src.common.exceptions import AppException, ExceptionType


class InventoryRecord:

    def __init__(self, product_id: str, quantity: int, timestamp: datetime, id: int | None = None) -> None:
        self._validate(product_id, quantity, timestamp)
        self.id = id
        self.product_id = product_id
        self.quantity = quantity
        self.timestamp = timestamp

    @staticmethod
    def _validate(product_id: str, quantity: int, timestamp: datetime) -> None:
        if not product_id or not product_id.strip():
            raise AppException(
                message="Product ID must not be empty",
                code="INVALID_PRODUCT_ID",
                exception_type=ExceptionType.BAD_REQUEST,
            )
        if quantity < 0:
            raise AppException(
                message="Quantity must be non-negative",
                code="INVALID_QUANTITY",
                exception_type=ExceptionType.BAD_REQUEST,
            )
        if timestamp is None:
            raise AppException(
                message="Timestamp is required",
                code="INVALID_TIMESTAMP",
                exception_type=ExceptionType.BAD_REQUEST,
            )
