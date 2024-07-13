import uuid
import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    name: str
    surname: str
    username: str
    phone_number: Optional[str] = Field(None, max_length=20)
    email: EmailStr
    image_path: Optional[str] = Field(None, max_length=128)


class UserCreate(UserBase):
    password: str


class UserUpdatePartial(UserBase):
    name: str | None = None
    surname: str | None = None
    username: str | None = None
    password: str | None = None
    phone_number: str | None = None
    email: EmailStr | None = None
    group_id: int | None = None
    image_path: str | None = None


class User(UserBase):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    role_id: int
    group_id: int | None = None
    is_blocked: bool = False
    active: bool = True


class CurrentUser(User):
    iat: datetime = None

    class Config:
        from_attributes = True
