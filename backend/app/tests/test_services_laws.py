import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app import models, schemas
from backend.app.database import Base
from backend.app.services import laws as law_service


@pytest.fixture(scope="function")
def db_session():
    engine = create_engine("sqlite:///:memory:", echo=False, future=True)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()


def test_create_law(db_session):
    law_in = schemas.LawCreate(
        code="ГК РФ", article="10", title="Злоупотребление правом"
    )
    law = law_service.create_law(db_session, law_in)
    assert law.id is not None
    assert law.code == "ГК РФ"


def test_update_law(db_session):
    law_in = schemas.LawCreate(
        code="АПК РФ", article="4", title="Право на обращение в суд"
    )
    law = law_service.create_law(db_session, law_in)
    update_data = schemas.LawUpdate(title="Обновленное название")
    updated_law = law_service.update_law(db_session, law.id, update_data)
    assert updated_law.title == "Обновленное название"


def test_delete_law(db_session):
    law_in = schemas.LawCreate(code="НК РФ", article="122", title="Неуплата налога")
    law = law_service.create_law(db_session, law_in)
    law_service.delete_law(db_session, law.id)
    assert db_session.query(models.Law).filter_by(id=law.id).first() is None
