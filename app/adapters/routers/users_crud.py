from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import db_session
from app.domain.schemas.user import User, UserCreate, UserUpdatePartial
from app.repositories.user_crud_repo import UserRepo

router = APIRouter(tags=["internal-users"], prefix="/internal-users")


@router.get("/all/")
async def get_users(
        session: Annotated[AsyncSession, db_session],
        user_repo: Annotated[UserRepo, Depends()],
) -> list[User]:
    return await user_repo.get_all_users(session=session)


@router.get("/user/")
async def get_user(
        user_id: UUID,
        session: Annotated[AsyncSession, db_session],
        user_repo: Annotated[UserRepo, Depends()],
) -> User:
    return await user_repo.get_user(user_id=user_id, session=session)


@router.post("/user-create/", status_code=status.HTTP_201_CREATED)
async def create_user(
        user_in: UserCreate,
        session: Annotated[AsyncSession, db_session],
        user_repo: Annotated[UserRepo, Depends()],
) -> User:
    return await user_repo.create_user(user_in=user_in, session=session)


@router.patch("/user-update/")
async def update_user(
        user_id: UUID,
        user_update: UserUpdatePartial,
        session: Annotated[AsyncSession, db_session],
        user_repo: Annotated[UserRepo, Depends()],
) -> User:
    return await user_repo.update_partial_user(user_id=user_id, user_update=user_update, session=session)


@router.delete("/user-delete/")
async def delete_user(
        user_id: UUID,
        session: Annotated[AsyncSession, db_session],
        user_repo: Annotated[UserRepo, Depends()],
) -> dict:
    return await user_repo.delete_user(user_id=user_id, session=session)
