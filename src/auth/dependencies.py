from datetime import datetime
from fastapi import Cookie, Depends

from src.auth import service
from src.auth.exceptions import EmailTaken, RefreshTokenNotValid
from src.auth.models import Token, User
from src.auth.schemas import AuthUser


async def valid_user_create(user: AuthUser) -> AuthUser:
    if await service.get_user_by_email(user.email):
        raise EmailTaken()

    return user


async def valid_refresh_token(
    refresh_token: str = Cookie(..., alias="refreshToken"),
) -> Token:
    db_refresh_token = await service.get_refresh_token(refresh_token)
    if not db_refresh_token:
        raise RefreshTokenNotValid()

    if not _is_valid_refresh_token(db_refresh_token):
        raise RefreshTokenNotValid()

    return db_refresh_token


async def valid_refresh_token_user(
    refresh_token: Token = Depends(valid_refresh_token),
) -> User:
    user = await service.get_user_by_id(refresh_token.user_id)
    if not user:
        raise RefreshTokenNotValid()

    return user


def _is_valid_refresh_token(db_refresh_token: Token) -> bool:
    return datetime.utcnow() <= db_refresh_token.expires_at
