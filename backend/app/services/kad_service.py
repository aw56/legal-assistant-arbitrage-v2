"""
Сервисный слой для интеграции с kad.arbitr.ru
"""

import httpx

from backend.app.integrations.kad_api import KadConfig


async def check_kad_health() -> dict:
    """
    Проверяет доступность сайта kad.arbitr.ru (HTTP HEAD-запрос)
    """
    cfg = KadConfig()
    url = cfg.base_url
    try:
        async with httpx.AsyncClient(timeout=cfg.timeout_s) as client:
            resp = await client.head(url)
            return {
                "status": "ok" if resp.status_code < 400 else "fail",
                "url": url,
                "code": resp.status_code,
            }
    except Exception as e:
        return {"status": "error", "url": url, "error": str(e)}
