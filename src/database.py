from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import (
    async_sessionmaker, create_async_engine, AsyncSession
)

from src.config import settings

__all__ = ("get_session", "Base", "DATABASE_URL")

DATABASE_URL = settings.DATABASE_URL

engine = create_async_engine(
    DATABASE_URL,
    echo=True
)

async_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
        await session.commit()


@as_declarative()
class Base:
    id: Mapped[int] = mapped_column(primary_key=True)
