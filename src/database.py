import uuid
from sqlalchemy import UUID, DateTime
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func
from sqlalchemy.ext.asyncio import (
    async_sessionmaker, create_async_engine, AsyncSession
)
from sqlalchemy.orm import DeclarativeBase

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


class Base(DeclarativeBase):
    id = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    created_at = mapped_column(DateTime, server_default=func.now(), nullable=False)
    updated_at = mapped_column(DateTime, server_onupdate=func.now())
