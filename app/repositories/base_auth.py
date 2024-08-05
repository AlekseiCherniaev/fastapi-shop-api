from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Response
from app.domain.schemas.user import User, UserUpdatePartial, CurrentUser, Token, CurrentUserUpdate


class BaseAuthRepo(ABC):

    @abstractmethod
    async def login_user(self, user: User) -> Token:
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
    async def get_current_user(self, payload: dict, user: User) -> CurrentUser:
        ...

    @abstractmethod
    async def update_current_user(self, payload: dict, user_update: UserUpdatePartial,
                                  session: AsyncSession) -> CurrentUserUpdate:
        ...

    @abstractmethod
    async def delete_current_user(self, payload: dict, session: AsyncSession) -> dict:
        ...
