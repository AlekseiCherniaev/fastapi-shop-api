from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.auth import get_current_token_payload
from app.dependencies.db import db_session
from app.domain.schemas.pagination_info import PaginationInfo
from app.domain.schemas.user import User, UserUpdatePartialAdmin
from app.repositories.user_repo import UserRepo

router = APIRouter(tags=["users"], prefix="/users")


@router.get("/all/", summary="Get all users", response_description="Users")
async def get_users(
        payload: Annotated[dict, Depends(get_current_token_payload)],
        pagination: Annotated[PaginationInfo, Depends()],
        session: Annotated[AsyncSession, db_session],
        user_repo: Annotated[UserRepo, Depends()],
) -> list[User]:
    """
    Get all users

    - **access_token** - Access token for check permissions
    - **page** - Page number
    - **limit** - Items per page
    - **filter** - Filter
    - **sort_by** - Sort by field
    - **order_by** - Decrease or increase order
    """
    return await user_repo.get_all_users(payload=payload, pagination=pagination, session=session)


@router.get("/user/", summary="Get user by id", response_description="User")
async def get_user(
        payload: Annotated[dict, Depends(get_current_token_payload)],
        user_id: UUID,
        session: Annotated[AsyncSession, db_session],
        user_repo: Annotated[UserRepo, Depends()],
) -> User:
    """
    Get user by id

    - **access_token** - Access token for check permissions
    - **user_id** - User id
    """
    return await user_repo.get_user(payload=payload, user_id=user_id, session=session)


@router.patch("/user-update/", summary="Update user", response_description="User")
async def update_user(
        payload: Annotated[dict, Depends(get_current_token_payload)],
        user_id: UUID,
        user_update: UserUpdatePartialAdmin,
        session: Annotated[AsyncSession, db_session],
        user_repo: Annotated[UserRepo, Depends()],
) -> User:
    """
    Update user by id

    - **access_token** - Access token for check permissions
    - **user_id** - User id
    - **name** - Name
    - **surname** - Surname
    - **email** - Email
    - **image_path** - Image path
    - **username** - Username
    - **password** - User password
    - **role_id** - User role id
    - **is_blocked** - Change user status
    """
    return await user_repo.update_partial_user(payload=payload, user_id=user_id, user_update=user_update,
                                               session=session)


@router.delete("/user-delete/", summary="Delete user", response_description="Success status")
async def delete_user(
        payload: Annotated[dict, Depends(get_current_token_payload)],
        user_id: UUID,
        session: Annotated[AsyncSession, db_session],
        user_repo: Annotated[UserRepo, Depends()],
) -> dict:
    """
    Delete user by id

    - **access_token** - Access token for check permissions
    - **user_id** - User id
    """
    return await user_repo.delete_user(payload=payload, user_id=user_id, session=session)
