import logging

from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.app import models, schemas

logger = logging.getLogger(__name__)


def create_decision(
    db: Session, decision: schemas.decision.DecisionCreate
) -> models.Decision:
    logger.info("Создание судебного решения: %s", decision.case_number)
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


def get_decisions(db: Session):
    return db.query(models.Decision).all()


def get_decision(db: Session, decision_id: int) -> models.Decision:
    decision = (
        db.query(models.Decision).filter(models.Decision.id == decision_id).first()
    )
    if not decision:
        raise HTTPException(status_code=404, detail="❌ Решение не найдено")
    return decision


def update_decision(
    db: Session, decision_id: int, decision_update: schemas.decision.DecisionUpdate
) -> models.Decision:
    decision = get_decision(db, decision_id)
    logger.info("Обновление судебного решения ID=%s", decision_id)
    for key, value in decision_update.dict(exclude_unset=True).items():
        setattr(decision, key, value)
    db.commit()
    db.refresh(decision)
    return decision


def delete_decision(db: Session, decision_id: int):
    decision = get_decision(db, decision_id)
    logger.info("Удаление судебного решения ID=%s", decision_id)
    db.delete(decision)
    db.commit()
    return {"status": "✅ Решение удалено"}
