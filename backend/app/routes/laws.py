from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.app import models
from backend.app.database import get_db
from backend.app.schemas.law import LawCreate, LawRead

router = APIRouter(prefix="/api/laws", tags=["laws"])

@router.post("/", response_model=LawRead, status_code=201)
def create_law(law: LawCreate, db: Session = Depends(get_db)):
    db_law = models.Law(**law.dict())
    db.add(db_law)
    db.commit()
    db.refresh(db_law)
    return db_law

@router.get("/", response_model=list[LawRead])
def list_laws(db: Session = Depends(get_db)):
    return db.query(models.Law).all()

@router.delete("/{law_id}", status_code=204)
def delete_law(law_id: int, db: Session = Depends(get_db)):
    law = db.query(models.Law).get(law_id)
    if not law:
        raise HTTPException(status_code=404, detail="Law not found")
    db.delete(law)
    db.commit()
    return
