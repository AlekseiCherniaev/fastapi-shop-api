import uuid
from typing import TYPE_CHECKING
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.domain.models import Base

if TYPE_CHECKING:
    from .role import Role


class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(16), nullable=False)
    surname: Mapped[str] = mapped_column(String(16), nullable=False)
    username: Mapped[str] = mapped_column(String(16), nullable=False, unique=True)
    password: Mapped[bytes] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(String(128), nullable=False, unique=True)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), nullable=False)
    image_path: Mapped[str] = mapped_column(String(128), nullable=True)
    is_blocked: Mapped[bool] = mapped_column(default=False, server_default='False')
    is_active: Mapped[bool] = mapped_column(default=False, server_default='False')

    roles: Mapped['Role'] = relationship(back_populates="users", lazy="selectin")
