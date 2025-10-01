from datetime import date

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app import models, schemas
from backend.app.database import Base
from backend.app.services import decisions as decision_service


@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:", echo=False, future=True)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()


def test_create_decision(db_session):
    decision_in = schemas.DecisionCreate(
        case_number="А40-12345/2025",
        court="Арбитражный суд г. Москвы",
        summary="Краткое резюме",
        date_decided=date.today(),
    )
    decision = decision_service.create_decision(db_session, decision_in)
    assert decision.id is not None
    assert decision.case_number == "А40-12345/2025"


def test_update_decision(db_session):
    decision_in = schemas.DecisionCreate(
        case_number="А40-67890/2025",
        court="АС МО",
        summary="Резюме",
    )
    decision = decision_service.create_decision(db_session, decision_in)
    update_data = schemas.DecisionUpdate(summary="Обновленное резюме")
    updated_decision = decision_service.update_decision(
        db_session, decision.id, update_data
    )
    assert updated_decision.summary == "Обновленное резюме"


def test_delete_decision(db_session):
    decision_in = schemas.DecisionCreate(
        case_number="А40-54321/2025",
        court="АС Санкт-Петербурга",
    )
    decision = decision_service.create_decision(db_session, decision_in)
    decision_service.delete_decision(db_session, decision.id)
    assert db_session.query(models.Decision).filter_by(id=decision.id).first() is None
