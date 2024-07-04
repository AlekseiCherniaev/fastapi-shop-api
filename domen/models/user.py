from uuid import uuid4, UUID

from pydantic import EmailStr
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from domen.models.base import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(32), nullable=False)
    surname: Mapped[str] = mapped_column(String(32), nullable=False)
    email: Mapped[EmailStr] = mapped_column(String(64), nullable=False, unique=True)
    username: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)
    password: Mapped[bytes] = mapped_column(nullable=False)
    image_path: Mapped[str] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True, server_default='True')
    is_blocked: Mapped[bool] = mapped_column(default=False, server_default='False')
