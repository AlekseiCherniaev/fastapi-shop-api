import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    name: str
    surname: str
    username: str
    email: EmailStr
    image_path: str | None = Field(None, max_length=128)


class UserCreate(UserBase):
    password: str


class UserUpdatePartial(UserBase):
    name: str | None = None
    surname: str | None = None
    username: str | None = None
    password: str | None = None
    email: EmailStr | None = None
    image_path: str | None = Field(None, max_length=128)


class User(UserBase):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    role_id: int
    is_blocked: bool
    is_active: bool

    class Config:
        from_attributes = True


class CurrentUser(UserBase):
    iat: datetime = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


class CurrentUserUpdate(BaseModel):
    user: User
    token: Token | None = None
