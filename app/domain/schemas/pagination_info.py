from enum import Enum

from pydantic import BaseModel, Field


class Order(Enum):
    ASC = "ASC"
    DESC = "DESC"


class Fields(Enum):
    id: int = "id"
    name: str = "name"
    surname: str = "surname"
    username: str = "username"
    email: str = "email"
    modified_at: str = "modified_at"
    created_at: str = "created_at"


class PaginationInfo(BaseModel):
    page: int = Field(1, ge=1)
    limit: int = Field(30, ge=1)
    filter_by_name: str | None = None
    sort_by: Fields | None = Fields.username
    order_by: Order = "DESC"
