from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import db_session
from app.domain.schemas.user import User, UserCreate, UserUpdatePartial
from app.repositories.user_crud_repo import UserRepo

router = APIRouter(tags=["internal-users"], prefix="/internal-users")


@router.get("/all/", summary="Get all users", response_description="All users")
async def get_users(
        session: Annotated[AsyncSession, db_session],
        user_repo: Annotated[UserRepo, Depends()],
) -> list[User]:
    """
    Get all users

    """
    return await user_repo.get_all_users(session=session)


@router.get("/user/", summary="Get user by id", response_description="User by id")
async def get_user(
        user_id: UUID,
        session: Annotated[AsyncSession, db_session],
        user_repo: Annotated[UserRepo, Depends()],
) -> User:
    """
    Get user by id

    - **user_id** - User id
    """
    return await user_repo.get_user(user_id=user_id, session=session)


@router.post("/user-create/", status_code=status.HTTP_201_CREATED, summary="Create user",
             response_description="User created")
async def create_user(
        user_in: UserCreate,
        session: Annotated[AsyncSession, db_session],
        user_repo: Annotated[UserRepo, Depends()],
) -> User:
    """
    Create user

    - **name** - Name
    - **surname** - Surname
    - **email** - Email
    - **image_path** - Image path
    - **username** - Username
    - **password** - User password
    """
    return await user_repo.create_user(user_in=user_in, session=session)


@router.patch("/user-update/", summary="Update user", response_description="User updated")
async def update_user(
        user_id: UUID,
        user_update: UserUpdatePartial,
        session: Annotated[AsyncSession, db_session],
        user_repo: Annotated[UserRepo, Depends()],
) -> User:
    """
    Update user by id

    - **user_id** - User id
    - **name** - Name
    - **surname** - Surname
    - **email** - Email
    - **image_path** - Image path
    - **username** - Username
    - **password** - User password
    """
    return await user_repo.update_partial_user(user_id=user_id, user_update=user_update, session=session)


@router.delete("/user-delete/", summary="Delete user", response_description="User deleted")
async def delete_user(
        user_id: UUID,
        session: Annotated[AsyncSession, db_session],
        user_repo: Annotated[UserRepo, Depends()],
) -> dict:
    """
    Delete user by id

    - **user_id** - User id
    """
    return await user_repo.delete_user(user_id=user_id, session=session)
