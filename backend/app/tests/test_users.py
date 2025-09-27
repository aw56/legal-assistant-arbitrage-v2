from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_create_user():
    response = client.post(
        "/api/users/",
        json={"username": "alice", "password": "secret", "role": "client"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "alice"
    assert data["role"] == "client"

def test_read_users():
    response = client.get("/api/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(user["username"] == "alice" for user in data)

def test_delete_user():
    # Удаляем пользователя "alice"
    response = client.delete("/api/users/1")
    assert response.status_code in (200, 204)
