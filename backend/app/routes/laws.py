from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app import models, schemas
from backend.app.database import get_db

router = APIRouter()


# 🔹 Создать закон
@router.post("/", response_model=schemas.law.Law)
def create_law(law: schemas.law.LawCreate, db: Session = Depends(get_db)):
    new_law = models.Law(**law.dict())
    db.add(new_law)
    db.commit()
    db.refresh(new_law)
    return new_law


# 🔹 Получить все законы
@router.get("/", response_model=List[schemas.law.Law])
def read_laws(db: Session = Depends(get_db)):
    return db.query(models.Law).all()


# 🔹 Получить закон по ID
@router.get("/{law_id}", response_model=schemas.law.Law)
def read_law(law_id: int, db: Session = Depends(get_db)):
    law = db.query(models.Law).filter(models.Law.id == law_id).first()
    if not law:
        raise HTTPException(status_code=404, detail="❌ Закон не найден")
    return law


# 🔹 Обновить закон (частично)
@router.patch("/{law_id}", response_model=schemas.law.Law)
def update_law(
    law_id: int, law_update: schemas.law.LawUpdate, db: Session = Depends(get_db)
):
    law = db.query(models.Law).filter(models.Law.id == law_id).first()
    if not law:
        raise HTTPException(status_code=404, detail="❌ Закон не найден")

    for key, value in law_update.dict(exclude_unset=True).items():
        setattr(law, key, value)

    db.commit()
    db.refresh(law)
    return law


# 🔹 Удалить закон
@router.delete("/{law_id}")
def delete_law(law_id: int, db: Session = Depends(get_db)):
    law = db.query(models.Law).filter(models.Law.id == law_id).first()
    if not law:
        raise HTTPException(status_code=404, detail="❌ Закон не найден")

    db.delete(law)
    db.commit()
    return {"status": "✅ Закон удалён"}
