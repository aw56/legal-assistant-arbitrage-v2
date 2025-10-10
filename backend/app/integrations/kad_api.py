# integrations/kad_api.py
"""
KAD (kad.arbitr.ru) API integration layer for Legal Assistant Arbitrage v2.

Design goals:
- Async-first using httpx.AsyncClient (compatible with FastAPI's event loop)
- Clear, typed Pydantic v2 models
- Built‑in timeouts, simple retries, and structured errors
- Minimal public surface: search_cases, get_case, download_document
- Sync convenience wrappers for scripts & tasks

Environment variables (12‑factor):
- KAD_BASE_URL (default: https://kad.arbitr.ru)
- KAD_API_KEY  (optional; if the instance requires an API key)
- KAD_TIMEOUT_S (default: 15)
- KAD_MAX_RETRIES (default: 2)

Notes:
- Real KAD endpoints and payloads vary; we normalize common fields we need.
- You can extend request/response models as the integration grows.
"""
from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import httpx
from pydantic import BaseModel, Field, ValidationError


# -----------------------------
# Pydantic response models
# -----------------------------
class CaseShort(BaseModel):
    id: str = Field(..., description="KAD internal case id")
    number: str = Field(..., description="Official case number")
    court: Optional[str] = Field(None, description="Court name or code")
    claim_subject: Optional[str] = None
    date_filed: Optional[str] = None  # ISO date


class CaseDetails(BaseModel):
    id: str
    number: str
    court: Optional[str] = None
    parties: List[str] = Field(default_factory=list)
    judge: Optional[str] = None
    status: Optional[str] = None
    hearings: List[Dict[str, Any]] = Field(default_factory=list)


class DocumentMeta(BaseModel):
    id: str
    case_id: str
    title: str
    doc_type: Optional[str] = None
    date: Optional[str] = None
    size_bytes: Optional[int] = None
    content_type: Optional[str] = None


# -----------------------------
# Exceptions
# -----------------------------
class KadError(Exception):
    """Base exception for KAD integration."""


class KadAuthError(KadError):
    pass


class KadNotFound(KadError):
    pass


class KadValidationError(KadError):
    pass


# -----------------------------
# Client
# -----------------------------
@dataclass
class KadConfig:
    base_url: str = os.getenv("KAD_BASE_URL", "https://kad.arbitr.ru")
    api_key: Optional[str] = os.getenv("KAD_API_KEY")
    timeout_s: float = float(os.getenv("KAD_TIMEOUT_S", "15"))
    max_retries: int = int(os.getenv("KAD_MAX_RETRIES", "2"))


class KadAPI:
    def __init__(self, config: Optional[KadConfig] = None):
        self.config = config or KadConfig()
        headers = {"Accept": "application/json"}
        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"
        self._client = httpx.AsyncClient(
            base_url=self.config.base_url.rstrip("/"),
            headers=headers,
            timeout=httpx.Timeout(self.config.timeout_s),
        )

    # --------- public API ---------
    async def search_cases(
        self,
        query: str,
        *,
        court: Optional[str] = None,
        page: int = 1,
        per_page: int = 20,
    ) -> List[CaseShort]:
        """Search cases by text query.
        NOTE: Endpoint path and params are representative; adjust to real KAD API.
        """
        params = {"q": query, "page": page, "per_page": per_page}
        if court:
            params["court"] = court
        data = await self._request_json("GET", "/api/cases/search", params=params)
        items = data.get("items", [])
        try:
            return [CaseShort(**self._normalize_case_short(raw)) for raw in items]
        except ValidationError as e:
            raise KadValidationError(str(e))

    async def get_case(self, case_id: str) -> CaseDetails:
        data = await self._request_json("GET", f"/api/cases/{case_id}")
        try:
            return CaseDetails(**self._normalize_case_details(data))
        except ValidationError as e:
            raise KadValidationError(str(e))

    async def download_document(self, doc_id: str) -> bytes:
        resp = await self._request(
            "GET", f"/api/documents/{doc_id}/download", expect_json=False
        )
        return resp.content

    async def aclose(self) -> None:
        await self._client.aclose()

    # --------- low-level helpers ---------
    async def _request_json(self, method: str, path: str, **kwargs) -> Dict[str, Any]:
        resp = await self._request(method, path, **kwargs)
        try:
            return resp.json()
        except Exception as e:  # pragma: no cover
            raise KadError(f"Invalid JSON from KAD at {path}: {e}")

    async def _request(
        self, method: str, path: str, *, expect_json: bool = True, **kwargs
    ) -> httpx.Response:
        last_exc: Optional[Exception] = None
        url = path if path.startswith("http") else f"{self._client.base_url}{path}"
        for attempt in range(self.config.max_retries + 1):
            try:
                resp = await self._client.request(method, url, **kwargs)
                if resp.status_code == 401:
                    raise KadAuthError("Unauthorized: check KAD_API_KEY")
                if resp.status_code == 404:
                    raise KadNotFound(f"Resource not found: {url}")
                resp.raise_for_status()
                return resp
            except (httpx.TimeoutException, httpx.TransportError) as e:
                last_exc = e
                if attempt < self.config.max_retries:
                    await asyncio.sleep(0.3 * (attempt + 1))
                    continue
                raise KadError(f"Network error after retries: {e}") from e
            except httpx.HTTPStatusError as e:  # pragma: no cover
                # Bubble up structured errors
                raise KadError(
                    f"KAD HTTP error {e.response.status_code}: {e.response.text}"
                ) from e
        # pragma: no cover
        if last_exc:
            raise KadError(f"Request failed: {last_exc}")
        raise KadError("Unknown request failure")

    # --------- normalizers (map KAD payloads -> internal models) ---------
    @staticmethod
    def _normalize_case_short(raw: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "id": str(raw.get("id") or raw.get("caseId") or ""),
            "number": raw.get("number") or raw.get("caseNumber") or "",
            "court": raw.get("court") or raw.get("courtName"),
            "claim_subject": raw.get("claimSubject") or raw.get("subject"),
            "date_filed": raw.get("dateFiled") or raw.get("registeredAt"),
        }

    @staticmethod
    def _normalize_case_details(raw: Dict[str, Any]) -> Dict[str, Any]:
        parties = raw.get("parties") or []
        if isinstance(parties, dict):
            parties = [p for p in parties.values() if isinstance(p, str)]
        return {
            "id": str(raw.get("id") or raw.get("caseId") or ""),
            "number": raw.get("number") or raw.get("caseNumber") or "",
            "court": raw.get("court") or raw.get("courtName"),
            "parties": parties,
            "judge": raw.get("judge") or raw.get("judgeName"),
            "status": raw.get("status"),
            "hearings": raw.get("hearings") or [],
        }


# -----------------------------
# Sync convenience wrappers
# -----------------------------
class KadSync:
    """Synchronous utility facade for scripts/CLI."""

    def __init__(self, config: Optional[KadConfig] = None):
        self._cfg = config or KadConfig()

    def search_cases(self, query: str, **kwargs) -> List[CaseShort]:
        return asyncio.run(self._async_search_cases(query, **kwargs))

    async def _async_search_cases(self, query: str, **kwargs) -> List[CaseShort]:
        client = KadAPI(self._cfg)
        try:
            return await client.search_cases(query, **kwargs)
        finally:
            await client.aclose()

    def get_case(self, case_id: str) -> CaseDetails:
        return asyncio.run(self._async_get_case(case_id))

    async def _async_get_case(self, case_id: str) -> CaseDetails:
        client = KadAPI(self._cfg)
        try:
            return await client.get_case(case_id)
        finally:
            await client.aclose()

    def download_document(self, doc_id: str, dst_path: Optional[str] = None) -> str:
        content = asyncio.run(self._async_download_document(doc_id))
        path = dst_path or f"document_{doc_id}.bin"
        with open(path, "wb") as f:
            f.write(content)
        return path

    async def _async_download_document(self, doc_id: str) -> bytes:
        client = KadAPI(self._cfg)
        try:
            return await client.download_document(doc_id)
        finally:
            await client.aclose()


__all__ = [
    "KadAPI",
    "KadSync",
    "KadConfig",
    "CaseShort",
    "CaseDetails",
    "DocumentMeta",
    "KadError",
    "KadAuthError",
    "KadNotFound",
    "KadValidationError",
]
