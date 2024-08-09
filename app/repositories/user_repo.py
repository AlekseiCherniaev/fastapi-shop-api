import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.schemas.pagination_info import PaginationInfo
from app.repositories.base_user import BaseUserRepo
from app.domain.schemas.user import User, UserUpdatePartialAdmin
from app.use_cases.user import UserUseCases


class UserRepo(BaseUserRepo):
    user_use_cases = UserUseCases()

    async def get_user(self, user_id: uuid.UUID, payload: dict, session: AsyncSession) -> User:
        return await self.user_use_cases.get_user(user_id=user_id, payload=payload, session=session)

    async def get_all_users(self, payload: dict, pagination: PaginationInfo, session: AsyncSession) -> list[User]:
        return await self.user_use_cases.get_all_users(payload=payload, session=session, pagination=pagination)

    async def update_partial_user(self, payload: dict, user_id: uuid.UUID, user_update: UserUpdatePartialAdmin,
                                  session: AsyncSession) -> User:
        return await self.user_use_cases.update_partial_user(payload=payload, user_id=user_id, user_update=user_update,
                                                             session=session)

    async def delete_user(self, payload: dict, user_id: uuid.UUID, session: AsyncSession) -> dict:
        return await self.user_use_cases.delete_user(payload=payload, user_id=user_id, session=session)
