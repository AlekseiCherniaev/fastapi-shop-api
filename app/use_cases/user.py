import uuid

from sqlalchemy import Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.exceptions import PermissionDeniedException
from app.dependencies.auth import get_current_user_from_token, get_role_from_user
from app.dependencies.user import get_user_by_id, user_update_partial
from app.dependencies.utils import make_statement
from app.domain.models import RoleEnum
from app.domain.schemas.pagination_info import PaginationInfo
from app.domain.schemas.user import UserUpdatePartialAdmin, User as UserSchema
from app.domain.models.user import User


class UserUseCases:
    async def get_user(self, user_id: uuid.UUID, payload: dict, session: AsyncSession) -> UserSchema:
        current_user = await get_current_user_from_token(payload=payload, session=session)
        role = await get_role_from_user(user=current_user, session=session)
        if role.name in (RoleEnum.ADMIN, RoleEnum.MODERATOR):
            return await get_user_by_id(user_id=user_id, session=session)
        else:
            raise PermissionDeniedException

    async def get_all_users(self, payload: dict, pagination: PaginationInfo, session: AsyncSession) -> list[UserSchema]:
        current_user = await get_current_user_from_token(payload=payload, session=session)
        role = await get_role_from_user(user=current_user, session=session)
        if role.name in (RoleEnum.ADMIN, RoleEnum.MODERATOR):
            statement = make_statement(pagination=pagination, model=User)
            result: Result = await session.execute(statement)
            return list(result.scalars().all())
        else:
            raise PermissionDeniedException

    async def update_partial_user(self, payload: dict, user_id: uuid.UUID, user_update: UserUpdatePartialAdmin,
                                  session: AsyncSession) -> UserSchema:
        current_user = await get_current_user_from_token(payload=payload, session=session)
        role = await get_role_from_user(user=current_user, session=session)
        if role.name is RoleEnum.ADMIN:
            user = await get_user_by_id(user_id=user_id, session=session)
            return await user_update_partial(user=user, session=session, user_update=user_update)
        else:
            raise PermissionDeniedException

    async def delete_user(self, payload: dict, user_id: uuid.UUID, session: AsyncSession) -> dict:
        current_user = await get_current_user_from_token(payload=payload, session=session)
        role = await get_role_from_user(user=current_user, session=session)
        if role.name is RoleEnum.ADMIN:
            user = await get_user_by_id(user_id=user_id, session=session)
            await session.delete(user)
            await session.commit()
            return {'message': 'User deleted successfully'}
        else:
            raise PermissionDeniedException
