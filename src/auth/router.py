from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from src.auth import jwt
from src.auth.schemas import JWTData, AccessTokenResponse, UserDetail, UserResponse
from src.auth.service import get_user_service, UserService

router = APIRouter()


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register_user(
        user_data: UserDetail,
        service: UserService = Depends(get_user_service),
) -> UserResponse:
    user = await service.create(user_data)
    print(user.is_admin)
    return UserResponse.from_orm(user)


@router.get("/users/me", response_model=UserResponse)
async def get_my_account(
        jwt_data: JWTData = Depends(jwt.parse_jwt_user_data),
        service: UserService = Depends(get_user_service),
) -> UserResponse:
    user = await service.get_by_id(jwt_data.user_id)
    return UserResponse.from_orm(user)


@router.post("/users/tokens", response_model=AccessTokenResponse)
async def auth_user(
        form_data: OAuth2PasswordRequestForm = Depends(),
        service: UserService = Depends(get_user_service),
) -> AccessTokenResponse:
    user = await service.authenticate(form_data)
    # TODO add create refresh

    return AccessTokenResponse(
        access_token=jwt.create_access_token(user=user),
        refresh_token=jwt.create_access_token(user=user),
    )
