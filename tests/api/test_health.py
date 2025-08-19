import pytest


@pytest.mark.asyncio
async def test_integration_health(client):
    r = await client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
