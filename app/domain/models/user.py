import uuid
from typing import TYPE_CHECKING
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.domain.models import Base

if TYPE_CHECKING:
    from .role import Role
    from .group import Group


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    surname: Mapped[str] = mapped_column(String(128), nullable=False)
    username: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    password: Mapped[bytes] = mapped_column(nullable=False)
    phone_number: Mapped[str] = mapped_column(String(20), )
    email: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"), nullable=True)
    image_path: Mapped[str] = mapped_column(String(128))
    is_blocked: Mapped[bool] = mapped_column(default=False, server_default='False')
    active: Mapped[bool] = mapped_column(default=True, server_default='True')

    roles: Mapped['Role'] = relationship(back_populates="users")
    groups: Mapped['Group'] = relationship(back_populates="users")
