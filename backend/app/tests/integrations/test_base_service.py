"""
backend/app/tests/integrations/test_base_service.py
---------------------------------------------------
Интеграционный тест для базового класса BaseIntegrationService.
v2.9 Integration & Intelligence Phase
© Aleksej, 2025
"""

import pytest
import respx
from app.integrations.base_service import BaseIntegrationService, IntegrationError
from httpx import HTTPStatusError, RequestError, Response


class DummyService(BaseIntegrationService):
    """Тестовый наследник BaseIntegrationService."""

    base_url = "https://example.com/api"
    service_name = "DummyService"

    async def fetch(self, *args, **kwargs):
        data = await self._request("GET", "demo")
        return data

    def parse(self, data):
        return {"ok": data.get("ok", False)}

    async def store(self, parsed):
        return parsed


@pytest.mark.integration
@respx.mock
@pytest.mark.asyncio
async def test_request_success(monkeypatch):
    """Проверка успешного запроса."""
    service = DummyService()
    respx.get("https://example.com/api/demo").mock(
        return_value=Response(200, json={"ok": True})
    )

    events = []

    def fake_log(service_name, level, message):
        events.append((service_name, level, message))

    monkeypatch.setattr(
        "app.integrations.integration_logger.log_integration_event", fake_log
    )

    result = await service._request("GET", "demo")
    assert result == {"ok": True}
    assert any("200" in msg for _, _, msg in events)


@pytest.mark.integration
@respx.mock
@pytest.mark.asyncio
async def test_request_http_error(monkeypatch):
    """Проверка обработки HTTP-ошибки."""
    service = DummyService()
    route = respx.get("https://example.com/api/demo").mock(
        return_value=Response(404, json={"detail": "not found"})
    )

    events = []

    def fake_log(service_name, level, message):
        events.append((service_name, level, message))

    monkeypatch.setattr(
        "app.integrations.integration_logger.log_integration_event", fake_log
    )

    with pytest.raises(IntegrationError):
        await service._request("GET", "demo")

    assert route.called
    assert any("HTTP error" in msg for _, _, msg in events)


@pytest.mark.integration
@pytest.mark.asyncio
async def test_request_network_error(monkeypatch):
    """Проверка обработки сетевой ошибки."""
    service = DummyService()

    async def mock_request(*_, **__):
        raise RequestError("Connection failed")

    async def dummy_json():
        return {"ok": True}

    monkeypatch.setattr("httpx.AsyncClient.request", mock_request)

    with pytest.raises(IntegrationError) as excinfo:
        await service._request("GET", "demo")

    assert "Connection failed" in str(excinfo.value)
