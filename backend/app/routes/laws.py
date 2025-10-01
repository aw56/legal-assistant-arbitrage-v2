from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.app import schemas
from backend.app.database import get_db
from backend.app.services import laws as law_service

router = APIRouter(tags=["laws"])


@router.post("/", response_model=schemas.Law, status_code=status.HTTP_201_CREATED)
def create_law(law: schemas.LawCreate, db: Session = Depends(get_db)):
    return law_service.create_law(db, law)


@router.get("/", response_model=list[schemas.Law])
def read_laws(db: Session = Depends(get_db)):
    return law_service.get_laws(db)


@router.get("/{law_id}", response_model=schemas.Law)
def read_law(law_id: int, db: Session = Depends(get_db)):
    return law_service.get_law(db, law_id)


@router.put("/{law_id}", response_model=schemas.Law)
def update_law(
    law_id: int, law_update: schemas.LawUpdate, db: Session = Depends(get_db)
):
    return law_service.update_law(db, law_id, law_update)


@router.delete("/{law_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_law(law_id: int, db: Session = Depends(get_db)):
    return law_service.delete_law(db, law_id)
