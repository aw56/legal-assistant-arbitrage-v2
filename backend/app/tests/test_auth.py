import httpx
import pytest


@pytest.mark.asyncio
async def test_register_and_login(client: httpx.Client):
    # === регистрация ===
    response = client.post(
        "/api/auth/register",
        json={"username": "apitest", "password": "testpass"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data

    # === логин ===
    response = client.post(
        "/api/auth/login",
        data={"username": "apitest", "password": "testpass"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data


@pytest.mark.asyncio
async def test_login_wrong_password(client: httpx.Client):
    # создаём пользователя
    client.post(
        "/api/auth/register",
        json={"username": "wronguser", "password": "rightpass"},
    )

    # пробуем войти с неверным паролем
    response = client.post(
        "/api/auth/login",
        data={"username": "wronguser", "password": "badpass"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"
