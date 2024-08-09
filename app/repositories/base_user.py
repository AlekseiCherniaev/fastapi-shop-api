import uuid
from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.schemas.pagination_info import PaginationInfo
from app.domain.schemas.user import User, UserUpdatePartialAdmin


class BaseUserRepo(ABC):

    @abstractmethod
    async def get_user(self, user_id: uuid.UUID, payload: dict, session: AsyncSession) -> User:
        ...

    @abstractmethod
    async def get_all_users(self, payload: dict, pagination: PaginationInfo, session: AsyncSession) -> list[User]:
        ...

    @abstractmethod
    async def update_partial_user(self, payload: dict,  user_id: uuid.UUID, user_update: UserUpdatePartialAdmin,
                                  session: AsyncSession) -> User:
        ...

    @abstractmethod
    async def delete_user(self, payload: dict,  user_id: uuid.UUID, session: AsyncSession) -> dict:
        ...
