from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.config.config import settings


class Database:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(url=url, echo=echo)
        self.session_factory = async_sessionmaker(
            bind=self.engine, autocommit=False, autoflush=False, expire_on_commit=False
        )

    async def session_dependency(self) -> AsyncSession:
        async with self.session_factory() as session:
            yield session


db = Database(url=settings.get_db_url(), echo=True)
