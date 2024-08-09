from fastapi import Response
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.exceptions import UserNotFoundException
from app.dependencies.auth import get_current_user_from_token
from app.dependencies.user import user_update_partial
from app.dependencies.utils import create_access_token, create_refresh_token
from app.domain.schemas.user import User, CurrentUser, UserUpdatePartial, Token, CurrentUserUpdate, UserBase


class AuthUseCases:
    async def login_user(self, user: User) -> Token:
        return Token(
            access_token=create_access_token(user=user),
            refresh_token=create_refresh_token(user=user),
            token_type="Bearer"
        )

    async def signup_user(self, user: User) -> Token:
        return Token(
            access_token=create_access_token(user=user),
            refresh_token=create_refresh_token(user=user),
            token_type="Bearer"
        )

    async def refresh_jwt(self, user: User) -> Token:
        return Token(
            access_token=create_access_token(user=user)
        )

    async def logout_user(self, response: Response) -> None:
        # TODO: Implement logout with adding token into Blacklist
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

    async def reset_password(self, email: EmailStr) -> None:
        # TODO: Implement reset password with publishing message to RabbitMQ
        pass

    async def get_current_user(self, payload: dict, user: User) -> CurrentUser:
        iat = payload.get("iat")
        user_schema = CurrentUser.model_validate(user)
        user_schema.iat = iat
        return user_schema

    async def update_current_user(self, payload: dict, user_update: UserUpdatePartial,
                                  session: AsyncSession) -> CurrentUserUpdate:
        user = await get_current_user_from_token(payload=payload, session=session)
        if not user:
            raise UserNotFoundException
        token = Token(
            access_token=create_access_token(user=user),
            refresh_token=create_refresh_token(user=user)
        ) if user_update.username and user_update.username != user.username else None
        user = await user_update_partial(user=user, user_update=user_update, session=session)
        user_schema = CurrentUserUpdate.model_validate(user)
        user_schema.token = token
        return user_schema

    async def delete_current_user(self, payload: dict, session: AsyncSession) -> dict:
        user = await get_current_user_from_token(payload=payload, session=session)
        if not user:
            raise UserNotFoundException

        await session.delete(user)
        await session.commit()
        return {'message': 'User deleted successfully'}
