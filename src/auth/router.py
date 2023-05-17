from fastapi import APIRouter, Depends, status

from src.auth import service
from src.auth.schemas import UserResponse, UserCreate
from src.auth.service import UserService

router = APIRouter()


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register_user(
    user_data: UserCreate,
    service: UserService = Depends(service.get_user_service),
) -> UserResponse:
    user = await service.create(user_data)
    return UserResponse.from_orm(user)
