from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.auth import validate_auth_user, get_current_auth_user, get_current_token_payload, \
    get_current_auth_user_for_refresh, http_bearer
from app.dependencies.db import db_session
from app.domain.schemas.user import User, UserCreate, UserUpdatePartial, CurrentUser, Token, CurrentUserUpdate
from app.repositories.auth_repo import AuthRepo
from app.repositories.user_crud_repo import UserRepo

router = APIRouter(tags=["auth"], prefix="/auth", dependencies=[Depends(http_bearer)])


@router.post("/login/")
async def login(
        user: Annotated[User, Depends(validate_auth_user)],
        auth_repo: Annotated[AuthRepo, Depends()],
) -> Token:
    return await auth_repo.login_user(user=user)


@router.post("/register/", status_code=status.HTTP_201_CREATED)
async def register(
        user_in: UserCreate,
        session: Annotated[AsyncSession, db_session],
        user_repo: Annotated[UserRepo, Depends()],
        auth_repo: Annotated[AuthRepo, Depends()],
) -> Token:
    return await auth_repo.signup_user(user=await user_repo.create_user(user_in=user_in, session=session))


@router.post("/refresh-token/")
async def refresh(
        user: Annotated[User, Depends(get_current_auth_user_for_refresh)],
        auth_repo: Annotated[AuthRepo, Depends()],
) -> Token:
    return await auth_repo.refresh_jwt(user=user)


@router.get("/logout/")
async def logout(
        response: Response,
        auth_repo: Annotated[AuthRepo, Depends()],
) -> None:
    return await auth_repo.logout_user(response=response)


@router.get("/me/")
async def current_user(
        payload: Annotated[dict, Depends(get_current_token_payload)],
        user: Annotated[User, Depends(get_current_auth_user)],
        auth_repo: Annotated[AuthRepo, Depends()],
) -> CurrentUser:
    return await auth_repo.get_current_user(payload=payload, user=user)


@router.patch("/update-me/")
async def update_me(
        payload: Annotated[dict, Depends(get_current_token_payload)],
        user_update: UserUpdatePartial,
        session: Annotated[AsyncSession, db_session],
        auth_repo: Annotated[AuthRepo, Depends()],
) -> CurrentUserUpdate:
    return await auth_repo.update_current_user(payload=payload, user_update=user_update, session=session)


@router.delete("/delete-me/")
async def delete_me(
        payload: Annotated[dict, Depends(get_current_token_payload)],
        session: Annotated[AsyncSession, db_session],
        auth_repo: Annotated[AuthRepo, Depends()],
) -> dict:
    return await auth_repo.delete_current_user(payload=payload, session=session)
