from typing import TYPE_CHECKING
from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.domain.models import Base

if TYPE_CHECKING:
    from .user import User


class RoleEnum(enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"


class Role(Base):
    __tablename__ = "roles"

    name: Mapped[str] = mapped_column(Enum(RoleEnum), unique=True, nullable=False, default=RoleEnum.USER)

    users: Mapped[list['User']] = relationship(back_populates="roles")
