from enum import Enum

from pydantic import BaseModel, Field


class Order(Enum):
    ASC = "ASC"
    DESC = "DESC"


class PaginationInfo(BaseModel):
    page: int = Field(1, ge=1)
    limit: int = Field(30, ge=1)

    filter_by_name: str | None = None

    sort_by: str | None = "username"

    order_by: Order = "DESC"
