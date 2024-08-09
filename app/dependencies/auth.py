from fastapi import Depends, Form
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.elements import or_

from app.config.exceptions import InvalidTokenException, UserNotFoundException, WrongPasswordException, \
    UserBlockedException
from app.dependencies.db import db_session
from app.dependencies.utils import decode_jwt, TOKEN_TYPE_FIELD, ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE, \
    validate_password
from app.domain.models import User, Role

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login/",
)
http_bearer = HTTPBearer(auto_error=False)


def get_current_token_payload(token: str = Depends(oauth2_scheme)) -> dict:
    return decode_jwt(token=token)


def validate_token_type(
        payload: dict,
        token_type: str,
) -> bool:
    current_token_type = payload.get(TOKEN_TYPE_FIELD)
    if current_token_type == token_type:
        return True
    else:
        raise InvalidTokenException


async def get_current_user_from_token(
        payload: dict,
        session: AsyncSession,
) -> User:
    username = payload.get("sub")
    if username:
        statement = select(User).where(User.username == username)
        result: Result = await session.execute(statement)
        user = result.scalar_one_or_none()
        if user:
            return user
        else:
            raise UserNotFoundException
    else:
        raise InvalidTokenException


async def get_role_from_user(
        user: User,
        session: AsyncSession,
) -> Role:
    statement = select(Role).where(Role.id == user.role_id)
    result: Result = await session.execute(statement)
    role = result.scalar_one_or_none()
    return role


def get_auth_user_from_token_of_type(token_type: str):
    async def auth_user_from_token_of_type(
            payload: dict = Depends(get_current_token_payload),
            session: AsyncSession = db_session,
    ) -> User:
        validate_token_type(payload=payload, token_type=token_type)
        return await get_current_user_from_token(payload=payload, session=session)

    return auth_user_from_token_of_type


get_current_auth_user = get_auth_user_from_token_of_type(ACCESS_TOKEN_TYPE)
get_current_auth_user_for_refresh = get_auth_user_from_token_of_type(REFRESH_TOKEN_TYPE)


async def validate_auth_user(
        username: str = Form(),
        password: str = Form(),
        session: AsyncSession = db_session,
) -> User:
    statement = select(User).where(or_(User.username == username, User.email == username))
    result: Result = await session.execute(statement)
    user = result.scalar_one_or_none()

    if not user:
        raise UserNotFoundException

    if not validate_password(
            password_to_validate=password,
            hashed_password=user.password,
    ):
        raise WrongPasswordException

    if user.is_blocked:
        raise UserBlockedException
    return user
