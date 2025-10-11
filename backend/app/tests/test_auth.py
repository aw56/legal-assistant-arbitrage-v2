import httpx
import pytest


@pytest.mark.asyncio
async def test_register_and_login(client: httpx.Client):
    # === регистрация ===
    response = client.post(
        "/api/auth/register",
        json={
            "username": "apitest",
            "password": "testpass",
            "email": "apitest@example.com",
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    # регистрация возвращает созданного пользователя (а не токен)
    assert data["username"] == "apitest"
    assert "id" in data

    # === логин ===
    response = client.post(
        "/api/auth/login",
        json={"username": "apitest", "password": "testpass"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data


@pytest.mark.asyncio
async def test_login_wrong_password(client: httpx.Client):
    # создаём пользователя
    client.post(
        "/api/auth/register",
        json={
            "username": "wronguser",
            "password": "rightpass",
            "email": "wronguser@example.com",
        },
    )

    # пробуем войти с неверным паролем
    response = client.post(
        "/api/auth/login",
        json={"username": "wronguser", "password": "badpass"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] in (
        "Incorrect username or password",
        "Invalid credentials",
    )
