from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app import models, schemas
from backend.app.database import get_db

router = APIRouter()


# 🔹 Создать судебное решение
@router.post("/", response_model=schemas.decision.Decision)
def create_decision(
    decision: schemas.decision.DecisionCreate, db: Session = Depends(get_db)
):
    db_decision = (
        db.query(models.Decision)
        .filter(models.Decision.case_number == decision.case_number)
        .first()
    )
    if db_decision:
        raise HTTPException(
            status_code=400, detail="❌ Решение с таким номером дела уже существует"
        )

    new_decision = models.Decision(**decision.dict())
    db.add(new_decision)
    db.commit()
    db.refresh(new_decision)
    return new_decision


# 🔹 Получить все решения
@router.get("/", response_model=List[schemas.decision.Decision])
def read_decisions(db: Session = Depends(get_db)):
    return db.query(models.Decision).all()


# 🔹 Получить решение по ID
@router.get("/{decision_id}", response_model=schemas.decision.Decision)
def read_decision(decision_id: int, db: Session = Depends(get_db)):
    decision = (
        db.query(models.Decision).filter(models.Decision.id == decision_id).first()
    )
    if not decision:
        raise HTTPException(status_code=404, detail="❌ Решение не найдено")
    return decision


# 🔹 Обновить решение (частично)
@router.patch("/{decision_id}", response_model=schemas.decision.Decision)
def update_decision(
    decision_id: int,
    decision_update: schemas.decision.DecisionUpdate,
    db: Session = Depends(get_db),
):
    decision = (
        db.query(models.Decision).filter(models.Decision.id == decision_id).first()
    )
    if not decision:
        raise HTTPException(status_code=404, detail="❌ Решение не найдено")

    for key, value in decision_update.dict(exclude_unset=True).items():
        setattr(decision, key, value)

    db.commit()
    db.refresh(decision)
    return decision


# 🔹 Удалить решение
@router.delete("/{decision_id}")
def delete_decision(decision_id: int, db: Session = Depends(get_db)):
    decision = (
        db.query(models.Decision).filter(models.Decision.id == decision_id).first()
    )
    if not decision:
        raise HTTPException(status_code=404, detail="❌ Решение не найдено")

    db.delete(decision)
    db.commit()
    return {"status": "✅ Решение удалено"}
