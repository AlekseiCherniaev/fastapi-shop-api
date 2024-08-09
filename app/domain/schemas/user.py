import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    name: str
    surname: str
    username: str
    email: EmailStr
    image_path: str | None

    class Config:
        from_attributes = True


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
    created_at: datetime
    modified_at: datetime = Field(default_factory=datetime.now)


class CurrentUser(UserBase):
    iat: datetime = None


class Token(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"


class CurrentUserUpdate(UserBase):
    token: Token | None = None


class UserUpdatePartialAdmin(UserUpdatePartial):
    role_id: int | None = Field(None, ge=0)
    is_blocked: bool | None = None
