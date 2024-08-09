from uuid import UUID

from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.exceptions import UserAlreadyExistsException, PasswordNotValidException, UserNotFoundException
from app.dependencies.utils import password_check_complexity, hash_password
from app.domain.models import User
from app.domain.schemas.user import UserUpdatePartial, UserUpdatePartialAdmin


async def get_user_by_id(user_id: UUID, session: AsyncSession) -> User:
    statement = select(User).where(User.id == user_id)
    result: Result = await session.execute(statement)
    user = result.scalar_one_or_none()
    if user:
        return user
    else:
        raise UserNotFoundException


async def user_update_partial(
        user_update: UserUpdatePartial | UserUpdatePartialAdmin,
        session: AsyncSession,
        user: User,
) -> User:
    if user_update.username and user_update.username != user.username:
        statement = select(User).where(User.username == user_update.username)
        check_user = (await session.execute(statement)).scalar_one_or_none()
        if check_user:
            raise UserAlreadyExistsException

    if user_update.email and user_update.email != user.email:
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
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
