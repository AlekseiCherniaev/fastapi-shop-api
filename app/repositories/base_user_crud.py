import uuid
from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.schemas.user import User, UserUpdatePartial, UserCreate


class BaseUserCrudRepo(ABC):

    @abstractmethod
    async def get_user(self, user_id: uuid.UUID, session: AsyncSession) -> User:
        ...

    @abstractmethod
    async def get_all_users(self, session: AsyncSession) -> list[User]:
        ...

    @abstractmethod
    async def create_user(self, user_in: UserCreate, session: AsyncSession) -> User:
        ...

    @abstractmethod
    async def update_partial_user(self, user_id: uuid.UUID, user_update: UserUpdatePartial,
                                  session: AsyncSession) -> User:
        ...

    @abstractmethod
    async def delete_user(self, user_id: uuid.UUID, session: AsyncSession) -> None:
        ...
