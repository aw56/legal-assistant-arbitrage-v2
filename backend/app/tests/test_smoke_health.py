import pytest
from httpx import ASGITransport, AsyncClient

from backend.app.main import app


@pytest.mark.smoke
@pytest.mark.asyncio
async def test_health_endpoint_returns_ok():
    """
    ✅ Smoke-тест: проверка эндпоинта /api/health.
    Ожидается HTTP 200 и JSON {"status": "ok"}.
    """
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.get("/api/health")

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert data.get("status") == "ok", f"Unexpected response JSON: {data}"
