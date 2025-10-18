"""
Base Integration Service (v2.9.6 Clean Path)
© Aleksej, 2025
"""

from typing import Any, Dict, Optional

# ✅ Импортируем модуль, чтобы monkeypatch корректно подменял функции
import app.integrations.integration_logger as integration_logger
import httpx


class IntegrationError(Exception):
    """Общее исключение интеграционного слоя."""


class BaseIntegrationService:
    """Базовый класс для интеграций (fetch / parse / store / log)."""

    base_url: str = ""
    service_name: str = "BaseService"

    async def _request(
        self,
        method: str,
        endpoint: str,
        *,
        params: Optional[dict] = None,
        data: Optional[dict] = None,
        headers: Optional[dict] = None,
        timeout: int = 10,
    ) -> Dict[str, Any]:
        """Асинхронный HTTP-запрос с логированием и обработкой ошибок."""
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                response = await client.request(
                    method, url, params=params, json=data, headers=headers
                )
                response.raise_for_status()
                result = response.json()

                integration_logger.log_integration_event(
                    self.service_name,
                    "INFO",
                    f"{method} {url} → {response.status_code}",
                )
                return result

        except httpx.HTTPStatusError as exc:
            integration_logger.log_integration_event(
                self.service_name,
                "ERROR",
                f"HTTP error {exc.response.status_code}: {url}",
            )
            raise IntegrationError(
                f"HTTP error {exc.response.status_code}: {url}"
            ) from exc

        except httpx.RequestError as exc:
            integration_logger.log_integration_event(
                self.service_name,
                "ERROR",
                f"Request failed: {exc}",
            )
            raise IntegrationError(f"Request failed: {exc}") from exc

    async def fetch(self, *args, **kwargs):
        raise NotImplementedError

    def parse(self, data: dict) -> dict:
        raise NotImplementedError

    async def store(self, parsed: dict):
        raise NotImplementedError
