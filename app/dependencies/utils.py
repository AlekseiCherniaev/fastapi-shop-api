import re
import uuid
import jwt
import bcrypt
from sqlalchemy import select, desc, Select

from app.config.config import settings
from datetime import timedelta, datetime

from app.config.exceptions import InvalidTokenException
from app.domain.models import User
from app.domain.schemas.pagination_info import PaginationInfo, Order


def password_check_complexity(password: str) -> bool:
    # reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
    password_regex = (
        r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
    )
    pattern = re.compile(password_regex)
    return bool(pattern.match(password))


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def validate_password(password_to_validate: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password_to_validate.encode(), hashed_password=hashed_password)


TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def encode_jwt(
        payload: dict,
        private_key: str = settings.PRIVATE_KEY_PATH.read_text(),
        algorithm: str = settings.ALGORITHM,
        expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        expire_timedelta: timedelta | None = None,
) -> str:
    to_encode = payload.copy()
    now = datetime.now()
    if expire_timedelta:
        expire_time = now + expire_timedelta
    else:
        expire_time = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire_time,
        iat=now,
        jti=str(uuid.uuid4())  # for jwt blacklist
    )
    encoded_jwt = jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm
    )
    return encoded_jwt


def decode_jwt(
        token: str | bytes,
        public_key: str = settings.PUBLIC_KEY_PATH.read_text(),
        algorithm: str = settings.ALGORITHM,
) -> dict:
    try:
        return jwt.decode(
            token,
            public_key,
            algorithms=[algorithm],
        )
    except Exception as e:
        raise InvalidTokenException


def create_jwt(
        token_type: str,
        token_data: dict,
        expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        expire_timedelta: timedelta | None = None,
) -> str:
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return encode_jwt(
        payload=jwt_payload,
        expire_minutes=expire_minutes,
        expire_timedelta=expire_timedelta,
    )


def create_access_token(user: User) -> str:
    jwt_payload = {
        "sub": user.username,
        "username": user.username,
        "email": user.email,
    }
    return create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )


def create_refresh_token(user: User) -> str:
    jwt_payload = {
        "sub": user.username
    }
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=jwt_payload,
        expire_timedelta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )


def make_statement(pagination: PaginationInfo, model) -> Select:
    statement = select(model)
    statement = (
        statement.offset(offset=(pagination.page - 1) * pagination.limit).limit(limit=pagination.limit)
        if pagination.filter_by_name is None
        else statement.filter(model.name == pagination.filter_by_name).limit(limit=pagination.limit)
    )
    statement = statement.order_by(pagination.sort_by.value) if pagination.order_by is Order.ASC else statement.order_by(
        desc(pagination.sort_by.value))
    return statement
