from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app import models, schemas
from backend.app.database import get_db

router = APIRouter()

@router.post("/", response_model=schemas.Law, status_code=201)
def create_law(law: schemas.LawCreate, db: Session = Depends(get_db)):
    db_law = models.Law(**law.model_dump())
    db.add(db_law)
    db.commit()
    db.refresh(db_law)
    return db_law


@router.get("/", response_model=list[schemas.Law])
def read_laws(db: Session = Depends(get_db)):
    return db.query(models.Law).all()


@router.delete("/{law_id}", status_code=204)
def delete_law(law_id: int, db: Session = Depends(get_db)):
    law = db.get(models.Law, law_id)
    if not law:
        raise HTTPException(status_code=404, detail="Law not found")
    db.delete(law)
    db.commit()
    return None
