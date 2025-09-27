from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_create_law():
    response = client.post(
        "/api/laws/",
        json={"code": "ГК РФ", "article": "10", "title": "Злоупотребление правом"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["code"] == "ГК РФ"
    assert data["article"] == "10"

def test_read_laws():
    response = client.get("/api/laws/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(law["article"] == "10" for law in data)

def test_delete_law():
    response = client.delete("/api/laws/1")
    assert response.status_code in (200, 204)
