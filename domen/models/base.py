from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[str] = mapped_column(nullable=False, default=func.now(),
                                            server_default=func.now())
    modified_at: Mapped[str] = mapped_column(nullable=False, default=func.func.now(),
                                             server_default=func.now())
