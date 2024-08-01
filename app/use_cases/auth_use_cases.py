from fastapi import Response
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.exceptions import UserNotFoundException, PasswordNotValidException
from app.config.logger import logger
from app.dependencies.auth_dependencies import get_current_user_from_token
from app.dependencies.user_dependencies import user_update_partial
from app.dependencies.utils import create_access_token, create_refresh_token
from app.domain.schemas.token import Token
from app.domain.schemas.user import User, CurrentUser, UserUpdatePartial


class AuthUseCases:
    async def login_user(self, user: User) -> Token:
        try:
            return Token(
                access_token=create_access_token(user=user),
                refresh_token=create_refresh_token(user=user),
                token_type="Bearer"
            )

        except Exception as e:
            logger.error(f"Error logining in: {str(e)}")

    async def signup_user(self, user: User) -> Token:
        try:
            return Token(
                access_token=create_access_token(user=user),
                refresh_token=create_refresh_token(user=user),
                token_type="Bearer"
            )

        except Exception as e:
            logger.error(f"Error signing up: {str(e)}")

    async def refresh_jwt(self, user: User) -> Token:
        try:
            return Token(
                access_token=create_access_token(user=user)
            )

        except Exception as e:
            logger.error(f"Error refreshing jwt: {str(e)}")

    async def logout_user(self, response: Response) -> None:
        # TODO: Implement logout with adding token into Blacklist
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

    async def reset_password(self, email: EmailStr) -> None:
        # TODO: Implement reset password with publishing message to RabbitMQ
        pass

    async def get_current_user(self, payload: dict, user: User) -> CurrentUser:
        try:
            if user:
                iat = payload.get("iat")
                user_schema = CurrentUser.model_validate(user)
                user_schema.iat = iat
                return user_schema

        except Exception as e:
            logger.error(f"Error getting current user: {str(e)}")

    async def update_current_user(self, payload: dict, user_update: UserUpdatePartial, session: AsyncSession) -> User:
        try:
            user = await get_current_user_from_token(payload=payload, session=session)
            if not user:
                raise UserNotFoundException

            return await user_update_partial(user=user, user_update=user_update, session=session)

        except PasswordNotValidException as e:
            logger.error(f"Password not valid: {str(e)}")
            raise e
        except UserNotFoundException as e:
            logger.error(f"User not found: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"Error updating current user: {str(e)}")

    async def delete_current_user(self, payload: dict, session: AsyncSession) -> None:
        try:
            user = await get_current_user_from_token(payload=payload, session=session)
            if not user:
                raise UserNotFoundException

            await session.delete(user)
            await session.commit()

        except UserNotFoundException as e:
            logger.error(f"User not found: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"Error deleting current user: {str(e)}")
