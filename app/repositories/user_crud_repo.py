import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.schemas.user import User, UserCreate, UserUpdatePartial
from app.repositories.base_user_crud import BaseUserCrudRepo
from app.use_cases.user_use_cases import UserUseCases


class UserCrudRepo(BaseUserCrudRepo):
    user_use_cases = UserUseCases()

    async def get_user(self, user_id: uuid.UUID, session: AsyncSession) -> User:
        return await self.user_use_cases.get_user_by_id(user_id=user_id, session=session)

    async def get_all_users(self, session: AsyncSession) -> list[User]:
        return await self.user_use_cases.get_all_users(session=session)

    async def create_user(self, user_in: UserCreate, session: AsyncSession) -> User:
        return await self.user_use_cases.create_user(user_in=user_in, session=session)

    async def update_partial_user(self, user_id: uuid.UUID, user_update: UserUpdatePartial,
                                  session: AsyncSession) -> User:
        return await self.user_use_cases.update_partial_user(user_id=user_id, user_update=user_update, session=session)

    async def delete_user(self, user_id: uuid.UUID, session: AsyncSession) -> None:
        return await self.user_use_cases.delete_user(user_id=user_id, session=session)
