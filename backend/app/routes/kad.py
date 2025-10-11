from fastapi import APIRouter, HTTPException, Query

from backend.app.integrations.kad_api import KadAPI, KadError
from backend.app.services.kad_service import check_kad_health

router = APIRouter()


@router.get("/search", tags=["kad"])
async def kad_search(
    q: str = Query(..., min_length=2, description="Текст или номер дела для поиска")
):
    """
    🔍 Поиск арбитражных дел через KAD API.
    """
    try:
        client = KadAPI()
        results = await client.search_cases(q)
        await client.aclose()
        return [case.model_dump() for case in results]
    except KadError as e:
        raise HTTPException(status_code=502, detail=str(e))


@router.get("/health", tags=["kad"])
async def kad_health():
    """
    🌐 Проверка доступности kad.arbitr.ru
    """
    return await check_kad_health()
