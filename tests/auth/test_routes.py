import pytest
from async_asgi_testclient import TestClient
from fastapi import status

from src.auth.constants import ErrorCode


@pytest.mark.asyncio
async def test_register(client: TestClient) -> None:
    resp = await client.post(
        "/auth/users",
        json={
            "email": "email@fake.com",
            "password": "123Aa!",
        },
    )
    resp_json = resp.json()

    assert resp.status_code == status.HTTP_201_CREATED
    assert resp_json == {"email": "email@fake.com"}


@pytest.mark.asyncio
async def test_register_email_taken(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    from src.auth.dependencies import service

    async def fake_getter(*args, **kwargs):
        return True

    monkeypatch.setattr(service, "get_user_by_email", fake_getter)

    resp = await client.post(
        "/auth/users",
        json={
            "email": "email@fake.com",
            "password": "123Aa!",
        },
    )
    resp_json = resp.json()

    assert resp.status_code == status.HTTP_400_BAD_REQUEST
    assert resp_json["detail"] == ErrorCode.EMAIL_TAKEN
