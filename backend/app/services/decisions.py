import logging
from datetime import datetime, timezone

from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.app import models, schemas

logger = logging.getLogger(__name__)


def create_decision(db: Session, decision: schemas.DecisionCreate) -> models.Decision:
    logger.info("Создание решения: %s", decision.case_number)

    # Проверка уникальности номера дела
    existing = (
        db.query(models.Decision)
        .filter(models.Decision.case_number == decision.case_number)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=400,
            detail="❌ Решение с таким номером дела уже существует",
        )

    new_decision = models.Decision(
        case_number=decision.case_number,
        court=decision.court,
        date_decided=decision.date_decided or datetime.now(timezone.utc),
        summary=decision.summary,
        law_id=decision.law_id,
        user_id=decision.user_id,
    )

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
    db: Session, decision_id: int, decision_update: schemas.DecisionUpdate
) -> models.Decision:
    decision = get_decision(db, decision_id)
    logger.info("Обновление решения ID=%s", decision_id)

    for key, value in decision_update.model_dump(exclude_unset=True).items():
        setattr(decision, key, value)

    # ⚡ обновляем timestamp
    decision.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(decision)
    return decision


def delete_decision(db: Session, decision_id: int) -> None:
    decision = get_decision(db, decision_id)
    logger.info("Удаление решения ID=%s", decision_id)
    db.delete(decision)
    db.commit()
