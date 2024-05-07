import uuid
from datetime import datetime, timedelta
from typing import Any

from pydantic import UUID4
from sqlalchemy import insert, select,update

from src import utils
from schemas import RolePermission,RolePermissionDB
from db import get_role_permission_by_id,update_role_permission,create_role_permissions  
from fastapi import status,HTTPException




# async def create_refresh_token(role) -> str:
#     if not refresh_token:
#         refresh_token = utils.generate_random_alphanum(64)

#     insert_query = refresh_tokens.insert().values(
#         uuid=uuid.uuid4(),
#         refresh_token=refresh_token,
#         expires_at=datetime.utcnow() + timedelta(seconds=auth_config.REFRESH_TOKEN_EXP),
#         user_id=user_id,
#     )
#     await execute(insert_query)

#     return refresh_token


# async def get_refresh_token(refresh_token: str) -> dict[str, Any] | None:
#     select_query = refresh_tokens.select().where(
#         refresh_tokens.c.refresh_token == refresh_token
#     )

#     return await fetch_one(select_query)


# async def expire_refresh_token(refresh_token_uuid: UUID4) -> None:
#     update_query = (
#         refresh_tokens.update()
#         .values(expires_at=datetime.utcnow() - timedelta(days=1))
#         .where(refresh_tokens.c.uuid == refresh_token_uuid)
#     )

#     await execute(update_query)


# async def authenticate_user(auth_data: AuthUser) -> dict[str, Any]:
#     user = await get_user_by_email(auth_data.email)
#     if not user:
#         raise InvalidCredentials()

#     if not check_password(auth_data.password, user["password"]):
#         raise InvalidCredentials()

#     return user
