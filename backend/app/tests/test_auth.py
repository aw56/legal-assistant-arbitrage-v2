def test_register_and_login(client):
    # 1. Регистрация нового пользователя
    response = client.post(
        "/api/auth/register",
        params={"username": "testuser", "password": "testpass"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["role"] == "client"

    # 2. Логин
    response = client.post(
        "/api/auth/login",
        data={"username": "testuser", "password": "testpass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data

    # 3. Доступ к защищённому эндпоинту
    headers = {"Authorization": f"Bearer {token_data['access_token']}"}
    response = client.get("/api/auth/me", headers=headers)
    assert response.status_code == 200
    me_data = response.json()
    assert me_data["username"] == "testuser"
    assert me_data["role"] == "client"


def test_login_wrong_password(client):
    # сначала регистрируем
    client.post(
        "/api/auth/register", params={"username": "user1", "password": "secret"}
    )
    # пробуем неверный пароль
    response = client.post(
        "/api/auth/login",
        data={"username": "user1", "password": "wrongpass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 401


def test_access_protected_without_token(client):
    response = client.get("/api/auth/me")
    assert response.status_code == 401
