from fastapi import APIRouter, BackgroundTasks, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from src.auth import jwt, service, utils
from src.auth.dependencies import (
    valid_refresh_token,
    valid_refresh_token_user,
    valid_user_create,
)
from src.auth.jwt import parse_jwt_user_data
from src.auth.models import Token, User
from src.auth.schemas import AccessTokenResponse, AuthUser, JWTData, UserResponse

router = APIRouter()


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register_user(
        auth_data: AuthUser = Depends(valid_user_create),
):
    user = await service.create_user(auth_data)
    return UserResponse.from_orm(user)


@router.get("/users/me", response_model=UserResponse)
async def get_my_account(
        jwt_data: JWTData = Depends(parse_jwt_user_data),
):
    user = await service.get_user_by_id(jwt_data.user_id)
    return UserResponse.from_orm(user)


@router.post("/users/tokens", response_model=AccessTokenResponse)
async def auth_user(
        response: Response,
        auth_data: OAuth2PasswordRequestForm = Depends()
) -> AccessTokenResponse:
    user = await service.authenticate_user(auth_data)
    refresh_token_value = await service.create_refresh_token(user_id=user.id)

    response.set_cookie(**utils.get_refresh_token_settings(refresh_token_value))

    return AccessTokenResponse(
        access_token=jwt.create_access_token(user=user),
        refresh_token=refresh_token_value,
    )


@router.put("/users/tokens", response_model=AccessTokenResponse)
async def refresh_tokens(
        worker: BackgroundTasks,
        response: Response,
        refresh_token: Token = Depends(valid_refresh_token),
        user: User = Depends(valid_refresh_token_user),
) -> AccessTokenResponse:
    refresh_token_value = await service.create_refresh_token(
        user_id=refresh_token.user_id
    )
    response.set_cookie(**utils.get_refresh_token_settings(refresh_token_value))

    worker.add_task(service.expire_refresh_token, refresh_token.uuid)
    return AccessTokenResponse(
        access_token=jwt.create_access_token(user=user),
        refresh_token=refresh_token_value,
    )


@router.delete("/users/tokens")
async def logout_user(
        response: Response,
        refresh_token: Token = Depends(valid_refresh_token),
) -> None:
    await service.expire_refresh_token(refresh_token.uuid)

    response.delete_cookie(
        **utils.get_refresh_token_settings(refresh_token["refresh_token"], expired=True)
    )
