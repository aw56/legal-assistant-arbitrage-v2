from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.app import models
from backend.app.database import get_db

router = APIRouter(prefix="/api", tags=["system"])


@router.post("/reset", summary="Полный сброс тестовых данных (для CI / Postman)")
def reset_database(db: Session = Depends(get_db)):
    """
    Удаляет все записи из таблиц users, laws, decisions.
    Не трогает Alembic и структуру БД.
    Используется для очистки перед автотестами Postman или pytest.
    """
    try:
        # Удаляем связи в правильном порядке (чтобы не нарушить FK)
        db.query(models.Decision).delete()
        db.query(models.Law).delete()
        db.query(models.User).delete()
        db.commit()
        return {"status": "reset done ✅"}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}
