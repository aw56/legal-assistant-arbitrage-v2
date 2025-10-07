from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter(prefix="/api/docs", tags=["docs"])


@router.get("/postman", summary="Скачать Postman коллекцию")
def get_postman_collection():
    path = Path("docs/postman_collection.json")
    if not path.exists():
        return {"detail": "❌ Коллекция не найдена. Сначала запусти make postman"}
    return FileResponse(
        path, filename="postman_collection.json", media_type="application/json"
    )
