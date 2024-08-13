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


@router.post("/login/", summary="Login user", response_description="Access token for user")
async def login(
        user: Annotated[User, Depends(validate_auth_user)],
        auth_repo: Annotated[AuthRepo, Depends()],
) -> Token:
    """
    Login user with username and password and return access token

    - **username** - Username
    - **password** - User password
    """
    return await auth_repo.login_user(user=user)


@router.post("/register/", status_code=status.HTTP_201_CREATED, summary="Register user",
             response_description="Access token for user")
async def register(
        user_in: UserCreate,
        session: Annotated[AsyncSession, db_session],
        user_repo: Annotated[UserRepo, Depends()],
        auth_repo: Annotated[AuthRepo, Depends()],
) -> Token:
    """
    Register user and return access token

    - **name** - Name
    - **surname** - Surname
    - **email** - Email
    - **image_path** - Image path
    - **username** - Username
    - **password** - User password
    """
    return await auth_repo.signup_user(user=await user_repo.create_user(user_in=user_in, session=session))


@router.post("/refresh-token/", summary="Refresh access token", response_description="Access token for user")
async def refresh(
        user: Annotated[User, Depends(get_current_auth_user_for_refresh)],
        auth_repo: Annotated[AuthRepo, Depends()],
) -> Token:
    """
    Refresh access token and return access token

    - **refresh_token** - Refresh token
    """
    return await auth_repo.refresh_jwt(user=user)


@router.get("/logout/", summary="Logout user", response_description="None")
async def logout(
        response: Response,
        auth_repo: Annotated[AuthRepo, Depends()],
) -> None:
    """
    Logout user and delete access token or put it in blacklist

    """
    return await auth_repo.logout_user(response=response)


@router.get("/me/", summary="Get current user", response_description="Current user")
async def current_user(
        payload: Annotated[dict, Depends(get_current_token_payload)],
        user: Annotated[User, Depends(get_current_auth_user)],
        auth_repo: Annotated[AuthRepo, Depends()],
) -> CurrentUser:
    """
    Get current user

    - **access_token** - Access token
    """
    return await auth_repo.get_current_user(payload=payload, user=user)


@router.patch("/update-me/", summary="Update current user", response_description="Current user")
async def update_me(
        payload: Annotated[dict, Depends(get_current_token_payload)],
        user_update: UserUpdatePartial,
        session: Annotated[AsyncSession, db_session],
        auth_repo: Annotated[AuthRepo, Depends()],
) -> CurrentUserUpdate:
    """
    Update current user

    - **access_token** - Access token
    - **name** - Name
    - **surname** - Surname
    - **email** - Email
    - **image_path** - Image path
    - **username** - Username
    - **password** - User password
    """
    return await auth_repo.update_current_user(payload=payload, user_update=user_update, session=session)


@router.delete("/delete-me/", summary="Delete current user", response_description="Success status")
async def delete_me(
        payload: Annotated[dict, Depends(get_current_token_payload)],
        session: Annotated[AsyncSession, db_session],
        auth_repo: Annotated[AuthRepo, Depends()],
) -> dict:
    """
    Delete current user

    - **access_token** - Access token
    """
    return await auth_repo.delete_current_user(payload=payload, session=session)
