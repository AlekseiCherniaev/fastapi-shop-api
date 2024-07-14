import uuid
from abc import ABC, abstractmethod
from fastapi import Response
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.schemas.pagination_info import PaginationInfo
from app.domain.schemas.token import Token
from app.domain.schemas.user import User, UserUpdatePartial, UserCreate, CurrentUser


class BaseRepo(ABC):

    @abstractmethod
    async def create_user(self, user: UserCreate, session: AsyncSession) -> User:
        ...

    @abstractmethod
    async def login_user(self, user: User) -> Token:
        ...

    @abstractmethod
    async def get_current_user(self, payload: dict, user: User) -> CurrentUser:
        ...

    @abstractmethod
    async def update_current_user(self, payload: dict, user_update: UserUpdatePartial, session: AsyncSession) -> User:
        ...

    @abstractmethod
    async def delete_current_user(self, payload: dict, session: AsyncSession) -> None:
        ...

    @abstractmethod
    async def signup_user(self, user: User) -> Token:
        ...

    @abstractmethod
    async def refresh_jwt(self, user: User) -> Token:
        ...

    @abstractmethod
    async def logout_user(self, response: Response) -> None:
        ...

    @abstractmethod
    async def get_user(self, user_id: uuid.UUID, payload: dict,
                       session: AsyncSession) -> User | None:
        ...

    @abstractmethod
    async def update_user(self, user_id: uuid.UUID, payload: dict, user_update: UserUpdatePartial,
                          session: AsyncSession) -> User:
        ...

    @abstractmethod
    async def get_all_users(self, pagination: PaginationInfo, payload: dict, session: AsyncSession) -> list[User]:
        ...

    @abstractmethod
    async def reset_password(self, email: EmailStr) -> None:
        ...
