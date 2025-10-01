from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.app import schemas
from backend.app.database import get_db
from backend.app.services import decisions as decision_service

router = APIRouter(tags=["decisions"])


@router.post("/", response_model=schemas.Decision, status_code=status.HTTP_201_CREATED)
def create_decision(decision: schemas.DecisionCreate, db: Session = Depends(get_db)):
    return decision_service.create_decision(db, decision)


@router.get("/", response_model=list[schemas.Decision])
def read_decisions(db: Session = Depends(get_db)):
    return decision_service.get_decisions(db)


@router.get("/{decision_id}", response_model=schemas.Decision)
def read_decision(decision_id: int, db: Session = Depends(get_db)):
    return decision_service.get_decision(db, decision_id)


@router.put("/{decision_id}", response_model=schemas.Decision)
def update_decision(
    decision_id: int,
    decision_update: schemas.DecisionUpdate,
    db: Session = Depends(get_db),
):
    return decision_service.update_decision(db, decision_id, decision_update)


@router.delete("/{decision_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_decision(decision_id: int, db: Session = Depends(get_db)):
    return decision_service.delete_decision(db, decision_id)
