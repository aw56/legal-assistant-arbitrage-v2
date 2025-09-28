from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app import models, schemas
from backend.app.database import get_db

router = APIRouter()


@router.post("/", response_model=schemas.Decision, status_code=201)
def create_decision(decision: schemas.DecisionCreate, db: Session = Depends(get_db)):
    db_decision = models.Decision(**decision.model_dump())
    db.add(db_decision)
    db.commit()
    db.refresh(db_decision)
    return db_decision


@router.get("/", response_model=list[schemas.Decision])
def read_decisions(db: Session = Depends(get_db)):
    return db.query(models.Decision).all()


@router.delete("/{decision_id}", status_code=204)
def delete_decision(decision_id: int, db: Session = Depends(get_db)):
    decision = db.get(models.Decision, decision_id)
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    db.delete(decision)
    db.commit()
    return None
