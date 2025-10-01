import logging

from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.app import models, schemas

logger = logging.getLogger(__name__)


def create_law(db: Session, law: schemas.LawCreate) -> models.Law:
    logger.info("Создание закона: %s %s", law.code, law.article)
    new_law = models.Law(**law.model_dump())
    db.add(new_law)
    db.commit()
    db.refresh(new_law)
    return new_law


def get_laws(db: Session):
    return db.query(models.Law).all()


def get_law(db: Session, law_id: int) -> models.Law:
    law = db.query(models.Law).filter(models.Law.id == law_id).first()
    if not law:
        raise HTTPException(status_code=404, detail="❌ Закон не найден")
    return law


def update_law(db: Session, law_id: int, law_update: schemas.LawUpdate) -> models.Law:
    law = get_law(db, law_id)
    logger.info("Обновление закона ID=%s", law_id)
    for key, value in law_update.model_dump(exclude_unset=True).items():
        setattr(law, key, value)
    db.commit()
    db.refresh(law)
    return law


def delete_law(db: Session, law_id: int) -> None:
    law = get_law(db, law_id)
    logger.info("Удаление закона ID=%s", law_id)
    db.delete(law)
    db.commit()
