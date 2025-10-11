def test_create_user(client):
    response = client.post(
        "/api/users/",
        json={
            "username": "alice",
            "password": "secret",
            "email": "alice@example.com",
            "role": "client",
        },
    )
    assert response.status_code in (200, 201)
    data = response.json()
    assert data["username"] == "alice"
    assert data["role"] == "client"
    assert "id" in data


def test_read_users(client):
    client.post(
        "/api/users/",
        json={
            "username": "bob",
            "password": "secret",
            "email": "bob@example.com",
            "role": "lawyer",
        },
    )
    response = client.get("/api/users/")
    assert response.status_code == 200
    data = response.json()
    assert any(user["username"] == "bob" for user in data)


def test_delete_user(client):
    response = client.post(
        "/api/users/",
        json={
            "username": "charlie",
            "password": "secret",
            "email": "charlie@example.com",
            "role": "client",
        },
    )
    user_id = response.json()["id"]

    response = client.delete(f"/api/users/{user_id}")
    assert response.status_code in (200, 204)
