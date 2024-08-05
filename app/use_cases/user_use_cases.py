from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from sqlalchemy.sql.expression import or_

from app.config.exceptions import UserAlreadyExistsException, PasswordNotValidException, UserNotFoundException
from app.dependencies.user_dependencies import user_update_partial
from app.dependencies.utils import password_check_complexity, hash_password
from app.domain.models import User, Role
from app.domain.schemas.user import UserCreate, UserUpdatePartial


class UserUseCases:
    async def get_user_by_id(self, user_id: UUID, session: AsyncSession) -> User:
        statement = select(User).where(User.id == user_id)
        result: Result = await session.execute(statement)
        user = result.scalar_one_or_none()
        if user:
            return user
        else:
            raise UserNotFoundException

    async def get_all_users(self, session: AsyncSession) -> list[User]:
        statement = select(User).order_by(User.username)
        result: Result = await session.execute(statement)
        users = result.scalars().all()
        return list(users)

    async def create_user(self, user_in: UserCreate, session: AsyncSession) -> User:
        statement = select(User).where(or_(User.username == user_in.username, User.email == user_in.email))
        user = (await session.execute(statement)).all()
        if user:
            raise UserAlreadyExistsException

        user_data = user_in.model_dump()
        if not password_check_complexity(user_data["password"]):
            raise PasswordNotValidException
        user_data["password"] = hash_password(user_data["password"])

        statement = select(Role).where(Role.name == "USER")
        role = (await session.execute(statement)).scalar_one_or_none()
        user_data["role_id"] = role.id

        user = User(**user_data)
        session.add(user)
        await session.commit()
        return user

    async def update_partial_user(self, user_id: UUID, user_update: UserUpdatePartial, session: AsyncSession) -> User:
        user = await self.get_user_by_id(user_id=user_id, session=session)
        if not user:
            raise UserNotFoundException
        user = await user_update_partial(user=user, user_update=user_update, session=session)
        return user

    async def delete_user(self, user_id: UUID, session: AsyncSession) -> dict:
        user = await self.get_user_by_id(user_id=user_id, session=session)
        if not user:
            raise UserNotFoundException

        await session.delete(user)
        await session.commit()
        return {'message': 'User deleted successfully'}
