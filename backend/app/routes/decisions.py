from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app import models
from backend.app.database import get_db
from backend.app.schemas.decision import DecisionCreate, DecisionRead

router = APIRouter(prefix="/api/decisions", tags=["decisions"])

@router.post("/", response_model=DecisionRead, status_code=201)
def create_decision(decision: DecisionCreate, db: Session = Depends(get_db)):
    db_decision = models.Decision(**decision.dict())
    db.add(db_decision)
    db.commit()
    db.refresh(db_decision)
    return db_decision

@router.get("/", response_model=list[DecisionRead])
def list_decisions(db: Session = Depends(get_db)):
    return db.query(models.Decision).all()

@router.delete("/{decision_id}", status_code=204)
def delete_decision(decision_id: int, db: Session = Depends(get_db)):
    decision = db.query(models.Decision).get(decision_id)
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    db.delete(decision)
    db.commit()
    return
