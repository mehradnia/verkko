from datetime import datetime

from pydantic import BaseModel, Field


class SearchInventoryRecordsRequestDto(BaseModel):
    productid: str = Field(min_length=1)
    starttimestamp: datetime | None = None
    endtimestamp: datetime | None = None
