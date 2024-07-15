import uuid

from httpx import Response
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.schemas.pagination_info import PaginationInfo
from app.domain.schemas.token import Token
from app.domain.schemas.user import User, UserCreate, CurrentUser, UserUpdatePartial
from app.repositories.base import BaseUserRepo
from app.use_cases.user_use_cases import UserUseCases


class UserRepo(BaseUserRepo):
    user_use_cases = UserUseCases()

    async def create_user(self, user: UserCreate, session: AsyncSession) -> User:
        return await self.user_use_cases.create_user(user=user, session=session)

    async def login_user(self, user: User) -> Token:
        return await self.user_use_cases.login_user(user=user)

    async def get_current_user(self, payload: dict, user: User) -> CurrentUser:
        return await self.user_use_cases.get_current_user(payload=payload, user=user)

    async def update_current_user(self, payload: dict, user_update: UserUpdatePartial, session: AsyncSession) -> User:
        return await self.user_use_cases.update_current_user(payload=payload, user_update=user_update, session=session)

    async def delete_current_user(self, payload: dict, session: AsyncSession) -> None:
        await self.user_use_cases.delete_current_user(payload=payload, session=session)

    async def signup_user(self, user: User) -> Token:
        return await self.user_use_cases.signup_user(user=user)

    async def refresh_jwt(self, user: User) -> Token:
        return await self.user_use_cases.refresh_jwt(user=user)

    async def logout_user(self, response: Response) -> None:
        await self.user_use_cases.logout_user(response=response)

    async def get_user(self, user_id: uuid.UUID, payload: dict, session: AsyncSession) -> User | None:
        return await self.user_use_cases.get_user(user_id=user_id, payload=payload, session=session)

    async def update_user(self, user_id: uuid.UUID, payload: dict, user_update: UserUpdatePartial,
                          session: AsyncSession) -> User:
        return await self.user_use_cases.update_user(user_id=user_id, payload=payload, user_update=user_update,
                                                     session=session)

    async def get_all_users(self, pagination: PaginationInfo, payload: dict, session: AsyncSession) -> list[User]:
        return await self.user_use_cases.get_all_users(pagination=pagination, payload=payload, session=session)

    async def reset_password(self, email: EmailStr) -> None:
        await self.user_use_cases.reset_password(email=email)
