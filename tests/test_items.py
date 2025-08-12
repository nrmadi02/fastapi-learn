import pytest


@pytest.mark.asyncio
async def test_create_and_list_items(client):
    r = await client.post(
        "/api/v1/auth/register", json={"email": "a@b.com", "password": "secret123"}
    )
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    r2 = await client.post("/api/v1/items/", json={"title": "Item 1"}, headers=headers)
    assert r2.status_code == 200

    r3 = await client.get("/api/v1/items/?limit=5&offset=0", headers=headers)
    assert r3.status_code == 200
    data = r3.json()
    assert isinstance(data, list) and len(data) >= 1
