from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_create_decision():
    response = client.post(
        "/api/decisions/",
        json={
            "case_number": "А40-12345/2025",
            "court": "АС г. Москвы",
            "summary": "Иск удовлетворён частично"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["case_number"] == "А40-12345/2025"

def test_read_decisions():
    response = client.get("/api/decisions/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(d["case_number"] == "А40-12345/2025" for d in data)

def test_delete_decision():
    response = client.delete("/api/decisions/1")
    assert response.status_code in (200, 204)
