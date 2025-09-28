#!/usr/bin/env python3
import os

BASE_DIR = "backend/app/tests"

PATCHES = {
    "test_users.py": """import pytest

def test_create_user(client):
    response = client.post(
        "/api/users/",
        json={"username": "alice", "password": "secret", "role": "client"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "alice"
    assert "id" in data


def test_read_users(client):
    client.post(
        "/api/users/",
        json={"username": "bob", "password": "secret", "role": "lawyer"},
    )
    response = client.get("/api/users/")
    assert response.status_code == 200
    data = response.json()
    assert any(user["username"] == "bob" for user in data)


def test_delete_user(client):
    response = client.post(
        "/api/users/",
        json={"username": "charlie", "password": "secret", "role": "client"},
    )
    user_id = response.json()["id"]

    response = client.delete(f"/api/users/{user_id}")
    assert response.status_code in (200, 204)
""",
    "test_laws.py": """import pytest

def test_create_law(client):
    response = client.post(
        "/api/laws/",
        json={"code": "ГК РФ", "article": "10", "title": "Злоупотребление правом"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["code"] == "ГК РФ"
    assert "id" in data


def test_read_laws(client):
    client.post(
        "/api/laws/",
        json={"code": "АПК РФ", "article": "4", "title": "Право на обращение в суд"},
    )
    response = client.get("/api/laws/")
    assert response.status_code == 200
    data = response.json()
    assert any(law["code"] == "АПК РФ" for law in data)


def test_delete_law(client):
    response = client.post(
        "/api/laws/",
        json={"code": "НК РФ", "article": "122", "title": "Неуплата налога"},
    )
    law_id = response.json()["id"]

    response = client.delete(f"/api/laws/{law_id}")
    assert response.status_code in (200, 204)
""",
    "test_decisions.py": """import pytest

def test_create_decision(client):
    response = client.post(
        "/api/decisions/",
        json={
            "case_number": "А40-12345/2025",
            "court": "АС г. Москвы",
            "summary": "Иск удовлетворён частично",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["case_number"] == "А40-12345/2025"
    assert "id" in data


def test_read_decisions(client):
    client.post(
        "/api/decisions/",
        json={
            "case_number": "А40-9876/2025",
            "court": "АС СПб",
            "summary": "Иск отклонён",
        },
    )
    response = client.get("/api/decisions/")
    assert response.status_code == 200
    data = response.json()
    assert any(dec["case_number"] == "А40-9876/2025" for dec in data)


def test_delete_decision(client):
    response = client.post(
        "/api/decisions/",
        json={
            "case_number": "А40-5555/2025",
            "court": "АС МО",
            "summary": "Производство прекращено",
        },
    )
    dec_id = response.json()["id"]

    response = client.delete(f"/api/decisions/{dec_id}")
    assert response.status_code in (200, 204)
""",
}


def main():
    for filename, content in PATCHES.items():
        path = os.path.join(BASE_DIR, filename)
        if os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"✅ Patched {path}")
        else:
            print(f"⚠️ File not found: {path}")


if __name__ == "__main__":
    main()
