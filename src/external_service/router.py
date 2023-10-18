from fastapi import APIRouter

from src.external_service.client import Client
from src.external_service.schemas import PublicAPIsResponse

router = APIRouter()


@router.get("/apis", response_model=PublicAPIsResponse)
async def get_public_apis() -> PublicAPIsResponse:
    cg_client = Client()

    return await cg_client.get_public_apis()
