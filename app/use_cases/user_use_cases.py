from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result
from sqlalchemy.sql.expression import or_

from app.config.exceptions import UserAlreadyExistsException, PasswordNotValidException, UserNotFoundException
from app.dependencies.utils import password_check_complexity, hash_password
from app.domain.models import User, Role
from app.config.logger import logger
from app.domain.schemas.user import UserCreate, UserUpdatePartial


class UserUseCases:
    async def get_user_by_id(self, user_id: UUID, session: AsyncSession) -> User:
        try:
            statement = select(User).where(User.id == user_id)
            result: Result = await session.execute(statement)
            user = result.scalar_one_or_none()
            if user:
                return user
            else:
                raise UserNotFoundException
        except UserNotFoundException as e:
            logger.error(f"User not found: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"Error fetching user by id: {str(e)}")
            raise e

    async def get_all_users(self, session: AsyncSession) -> list[User]:
        try:
            statement = select(User).order_by(User.username)
            result: Result = await session.execute(statement)
            users = result.scalars().all()
            return list(users)
        except Exception as e:
            logger.error(f"Error fetching all users: {str(e)}")

    async def create_user(self, user_in: UserCreate, session: AsyncSession) -> User:
        try:
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

        except UserAlreadyExistsException as e:
            logger.error(f"User already exists: {str(e)}")
            raise e
        except PasswordNotValidException as e:
            logger.error(f"Password complexity error: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")

    async def update_partial_user(self, user_id: UUID, user_update: UserUpdatePartial, session: AsyncSession) -> User:
        try:
            user = await self.get_user_by_id(user_id=user_id, session=session)
            if not user:
                raise UserNotFoundException

            if user_update.username and user_update.username != user.username:
                statement = select(User).where(User.username == user_update.username)
                check_user = (await session.execute(statement)).scalar_one_or_none()
                if check_user:
                    raise UserAlreadyExistsException

            if user_update.username and user_update.email != user.email:
                statement = select(User).where(User.email == user_update.email)
                check_user = (await session.execute(statement)).scalar_one_or_none()
                if check_user:
                    raise UserAlreadyExistsException

            user_data = user_update.model_dump(exclude_unset=True)
            if user_data.get("password"):
                if not password_check_complexity(user_data["password"]):
                    raise PasswordNotValidException
                user_data["password"] = hash_password(user_data["password"])

            for key, value in user_data.items():
                if user_data.get(key):
                    setattr(user, key, value)
            await session.commit()
            return user

        except UserNotFoundException as e:
            logger.error(f"User not found: {str(e)}")
            raise e
        except UserAlreadyExistsException as e:
            logger.error(f"User already exists: {str(e)}")
            raise e
        except PasswordNotValidException as e:
            logger.error(f"Password complexity error: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"Error updating user: {str(e)}")

    async def delete_user(self, user_id: UUID, session: AsyncSession) -> None:
        try:
            user = await self.get_user_by_id(user_id=user_id, session=session)
            if not user:
                raise UserNotFoundException

            await session.delete(user)
            await session.commit()

        except UserNotFoundException as e:
            logger.error(f"User not found: {str(e)}")
            raise e
        except Exception as e:
            logger.error(f"Error deleting user: {str(e)}")
