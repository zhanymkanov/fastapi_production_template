import datetime

from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from functools import lru_cache
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt
from src.auth.config import auth_config
from src.auth.schemas import UserDetail, UserBase
from src.auth.security import hash_password, check_password
from src.auth.models import User
from src.auth.exceptions import EmailTaken, InvalidCredentials
from src.database import get_session


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: UserDetail) -> User:
        user_exist = await self.get_by_username_or_email(user)

        if user_exist:
            raise EmailTaken

        user_data = user.dict()
        password = user_data.pop("password")
        new_user = User(**user_data)
        new_user.password = hash_password(password)
        self.session.add(new_user)
        await self.session.commit()
        return new_user

    async def get_by_email(self, email: str) -> User | None:
        user = await self.session.scalar(
            select(User).where(User.email == email)
        )
        return user

    async def get_by_username_or_email(
            self, user: OAuth2PasswordRequestForm | UserBase
    ) -> User | None:
        user = await self.session.scalar(
            select(User).where(
                (User.username == user.username) |
                (User.email == user.username)
            )
        )
        return user

    async def get_by_id(self, id: int) -> User | None:
        user = await self.session.scalar(
            select(User).where(User.id == id)
        )
        return user

    async def authenticate(self, form_data: OAuth2PasswordRequestForm) -> User:
        user = await self.get_by_username_or_email(form_data)
        if user is None:
            raise InvalidCredentials
        if not check_password(form_data.password, user.password):
            raise InvalidCredentials

        return user


class JWTService:
    def __init__(self, cash):
        self.cash = cash

    @staticmethod
    def create_access_token(user: User):
        jwt_data = {
            "sub": str(user.id),
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=auth_config.JWT_EXP),
            "is_admin": user.is_admin,
        }

        return jwt.encode(jwt_data, auth_config.JWT_SECRET, algorithm=auth_config.JWT_ALG)

    def create_refresh_token(self, user: User):
        pass

    def block_access_token(self):
        pass


@lru_cache()
def get_user_service(
        session: AsyncSession = Depends(get_session),
) -> UserService:
    return UserService(session=session)
