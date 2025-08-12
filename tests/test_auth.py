import pytest


@pytest.mark.asyncio
async def test_register_and_login(client):
    r = await client.post(
        "/api/v1/auth/register", json={"email": "u@e.com", "password": "secret123"}
    )
    assert r.status_code == 200
    token = r.json()["access_token"]
    assert token

    r2 = await client.post(
        "/api/v1/auth/login", json={"email": "u@e.com", "password": "secret123"}
    )
    assert r2.status_code == 200
    assert r2.json()["access_token"]
