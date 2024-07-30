from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import db_session
from app.domain.schemas.user import User, UserCreate, UserUpdatePartial
from app.repositories.user_crud_repo import UserCrudRepo

router = APIRouter(tags=["users"], prefix="/internal/users")


@router.get("/")
async def get_users(
        session: AsyncSession = db_session,
        user_repo: UserCrudRepo = Depends(),
) -> list[User]:
    return await user_repo.get_all_users(session=session)


@router.get("/user/")
async def get_user(
        user_id: UUID,
        session: AsyncSession = db_session,
        user_repo: UserCrudRepo = Depends(),
) -> User:
    return await user_repo.get_user(user_id=user_id, session=session)


@router.post("/user-create/")
async def create_user(
        user_in: UserCreate,
        session: AsyncSession = db_session,
        user_repo: UserCrudRepo = Depends(),
) -> User:
    return await user_repo.create_user(user_in=user_in, session=session)


@router.patch("/user-update/")
async def update_user(
        user_id: UUID,
        user_update: UserUpdatePartial,
        session: AsyncSession = db_session,
        user_repo: UserCrudRepo = Depends(),
) -> User:
    return await user_repo.update_partial_user(user_id=user_id, user_update=user_update, session=session)


@router.delete("/user-delete/")
async def delete_user(
        user_id: UUID,
        session: AsyncSession = db_session,
        user_repo: UserCrudRepo = Depends(),
) -> None:
    return await user_repo.delete_user(user_id=user_id, session=session)
