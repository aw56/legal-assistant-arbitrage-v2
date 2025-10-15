"""Pytest suite for integrations.kad_api
Uses respx to mock httpx.AsyncClient.
Run: `pytest -q tests/test_kad_api.py`
"""

import os
import pathlib

import httpx
import pytest
import respx

from backend.app.integrations.kad_api import (
    CaseDetails,
    CaseShort,
    KadAPI,
    KadAuthError,
    KadConfig,
    KadNotFound,
    KadSync,
)

BASE = "https://kad.example.local"


@pytest.fixture
async def client():
    cfg = KadConfig(base_url=BASE, api_key="test")
    api = KadAPI(cfg)
    try:
        yield api
    finally:
        await api.aclose()


@respx.mock
@pytest.mark.asyncio
async def test_search_cases_ok(client):
    route = respx.get(f"{BASE}/api/cases/search").mock(
        return_value=httpx.Response(
            200,
            json={
                "items": [
                    {
                        "id": "123",
                        "caseNumber": "A40-1/2024",
                        "courtName": "АС г. Москвы",
                    },
                    {"id": "124", "number": "A40-2/2024", "court": "АС г. Москвы"},
                ]
            },
        )
    )
    items = await client.search_cases("A40")
    assert len(items) == 2
    assert isinstance(items[0], CaseShort)
    assert items[0].number == "A40-1/2024"
    assert route.called


@respx.mock
@pytest.mark.asyncio
async def test_get_case_ok(client):
    respx.get(f"{BASE}/api/cases/123").mock(
        return_value=httpx.Response(
            200,
            json={
                "caseId": "123",
                "caseNumber": "A40-1/2024",
                "courtName": "АС г. Москвы",
                "parties": ["ИСТЕЦ", "ОТВЕТЧИК"],
                "judgeName": "Судья Иванов",
                "status": "В производстве",
                "hearings": [{"date": "2024-03-01", "result": "назначено"}],
            },
        )
    )
    case = await client.get_case("123")
    assert isinstance(case, CaseDetails)
    assert case.id == "123"
    assert case.number == "A40-1/2024"
    assert case.judge == "Судья Иванов"


@respx.mock
@pytest.mark.asyncio
async def test_download_document_ok(client, tmp_path: pathlib.Path):
    respx.get(f"{BASE}/api/documents/42/download").mock(
        return_value=httpx.Response(200, content=b"PDFDATA")
    )
    content = await client.download_document("42")
    assert content == b"PDFDATA"


@respx.mock
@pytest.mark.asyncio
async def test_404_raises_not_found(client):
    respx.get(f"{BASE}/api/cases/999").mock(return_value=httpx.Response(404))
    with pytest.raises(KadNotFound):
        await client.get_case("999")


@respx.mock
@pytest.mark.asyncio
async def test_401_raises_auth(client):
    respx.get(f"{BASE}/api/cases/secure").mock(return_value=httpx.Response(401))
    with pytest.raises(KadAuthError):
        await client.get_case("secure")


def test_sync_facade(tmp_path: pathlib.Path, monkeypatch):
    # Use respx with context manager + explicit client inside facade
    import respx as _respx

    base = BASE
    cfg = KadConfig(base_url=base, api_key="x")
    sync = KadSync(cfg)

    with _respx.mock as router:
        router.get(f"{base}/api/cases/search").mock(
            return_value=httpx.Response(
                200, json={"items": [{"id": "1", "number": "A40-1/24"}]}
            )
        )
        items = sync.search_cases("A40")
        assert items[0].number == "A40-1/24"

        router.get(f"{base}/api/documents/7/download").mock(
            return_value=httpx.Response(200, content=b"BIN")
        )
        dst = tmp_path / "doc.bin"
        out = sync.download_document("7", dst_path=str(dst))
        assert os.path.exists(out)
        with open(out, "rb") as f:
            assert f.read() == b"BIN"
