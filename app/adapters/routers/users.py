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


@router.get("/all/")
async def get_users(
        payload: Annotated[dict, Depends(get_current_token_payload)],
        pagination: Annotated[PaginationInfo, Depends()],
        session: Annotated[AsyncSession, db_session],
        user_repo: Annotated[UserRepo, Depends()],
) -> list[User]:
    return await user_repo.get_all_users(payload=payload, pagination=pagination, session=session)


@router.get("/user/")
async def get_user(
        payload: Annotated[dict, Depends(get_current_token_payload)],
        user_id: UUID,
        session: Annotated[AsyncSession, db_session],
        user_repo: Annotated[UserRepo, Depends()],
) -> User:
    return await user_repo.get_user(payload=payload, user_id=user_id, session=session)


@router.patch("/user-update/")
async def update_user(
        payload: Annotated[dict, Depends(get_current_token_payload)],
        user_id: UUID,
        user_update: UserUpdatePartialAdmin,
        session: Annotated[AsyncSession, db_session],
        user_repo: Annotated[UserRepo, Depends()],
) -> User:
    return await user_repo.update_partial_user(payload=payload, user_id=user_id, user_update=user_update,
                                               session=session)


@router.delete("/user-delete/")
async def delete_user(
        payload: Annotated[dict, Depends(get_current_token_payload)],
        user_id: UUID,
        session: Annotated[AsyncSession, db_session],
        user_repo: Annotated[UserRepo, Depends()],
) -> dict:
    return await user_repo.delete_user(payload=payload, user_id=user_id, session=session)
