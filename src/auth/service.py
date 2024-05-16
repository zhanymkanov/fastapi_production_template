
from typing import Any

from src.auth.security import check_password
from src.auth.exceptions import InvalidCredentials
from src.auth.schemas import AuthUser
from src.auth.db import get_user_by_id,get_user_by_email
from src.auth.schemas import JWTData
from fastapi import Depends
from src.auth.jwt import parse_jwt_user_data

async def get_auth_account(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
) -> dict[str, str]:
    user = await get_user_by_id(jwt_data.user_id)

    return {
        "email": user["email"],
    }
async def authenticate_user(auth_data: AuthUser) -> dict[str, Any]:
    user = await get_user_by_email(auth_data.email)
    if not user:
        raise InvalidCredentials()

    if not check_password(auth_data.password, user["password"]):
        raise InvalidCredentials()

    return user

async def authenticate_user(jwt_data: JWTData = Depends(parse_jwt_user_data)) -> dict[str, Any]:
    user = await get_user_by_id(jwt_data.id)
    if not user:
        raise InvalidCredentials()

    return user
