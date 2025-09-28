import pytest

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
