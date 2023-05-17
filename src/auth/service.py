from sqlalchemy import select
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.schemas import UserCreate
from src.auth.security import hash_password
from src.auth.models import User
from functools import lru_cache
from src.auth.exceptions import EmailTaken
from src.database import get_session


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: UserCreate) -> User:
        user_exist = (
                await self.get_by_email(user.email)
                or await self.get_by_username(user.username)
        )
        if user_exist:
            raise EmailTaken

        user_data = user.dict()
        password = user_data.pop("password")
        new_user = User(**user_data)
        new_user.password = hash_password(password)
        self.session.add(new_user)
        return new_user

    async def get_by_email(self, email: str) -> User:
        user = await self.session.scalar(
            select(User).where(User.email == email)
        )
        return user

    async def get_by_username(self, username: str) -> User:
        user = await self.session.scalar(
            select(User).where(User.username == username)
        )
        return user


@lru_cache()
def get_user_service(
        session: AsyncSession = Depends(get_session),
) -> UserService:
    return UserService(session=session)
