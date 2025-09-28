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
