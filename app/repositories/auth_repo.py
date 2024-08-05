from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models import User
from app.domain.schemas.user import UserUpdatePartial, CurrentUser, Token, CurrentUserUpdate
from app.repositories.base_auth import BaseAuthRepo
from app.use_cases.auth_use_cases import AuthUseCases


class AuthRepo(BaseAuthRepo):
    auth_use_cases = AuthUseCases()

    async def login_user(self, user: User) -> Token:
        return await self.auth_use_cases.login_user(user=user)

    async def signup_user(self, user: User) -> Token:
        return await self.auth_use_cases.signup_user(user=user)

    async def refresh_jwt(self, user: User) -> Token:
        return await self.auth_use_cases.refresh_jwt(user=user)

    async def logout_user(self, response: Response) -> None:
        return await self.auth_use_cases.logout_user(response=response)

    async def get_current_user(self, payload: dict, user: User) -> CurrentUser:
        return await self.auth_use_cases.get_current_user(payload=payload, user=user)

    async def update_current_user(self, payload: dict, user_update: UserUpdatePartial,
                                  session: AsyncSession) -> CurrentUserUpdate:
        return await self.auth_use_cases.update_current_user(payload=payload, user_update=user_update, session=session)

    async def delete_current_user(self, payload: dict, session: AsyncSession) -> dict:
        return await self.auth_use_cases.delete_current_user(payload=payload, session=session)
