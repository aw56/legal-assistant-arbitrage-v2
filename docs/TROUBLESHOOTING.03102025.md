Вот подробная “послематчевая” документация: что сделали, с какими проблемами столкнулись, как диагностировали и чем всё закончилось. Сохрани (и положи в `docs/incident-auth-and-network.md`, если удобно) — пригодится как runbook.

# 1) Краткий итог

- ✅ Backend поднят в Docker, внешний доступ по `http://<ваш_IP>:8080` работает.
- ✅ БД PostgreSQL и миграции Alembic применяются.
- ✅ Базовые эндпоинты живы: `/api/health`, `/api/auth/register`, `/api/auth/login`, `/api/auth/me`.
- ✅ Регистрация → логин → запрос текущего пользователя с JWT — проходит.
- ✅ Postman-коллекция собрана, окружение настроено (base_url, access_token), все три запроса проверены.

# 2) Архитектура развертывания (prod compose)

- Контейнер **backend** (Uvicorn) слушает **8000** внутри контейнера.
- На хосте проброшен порт **8080 → 8000** (см. `docker-compose.prod.yml`).
- БД **PostgreSQL** в отдельном контейнере, том `pgdata`.
- Доступ снаружи — только на 8080/TCP. **Важно:** провайдерский FW должен пропускать 8080 к вашему серверу.

# 3) Хронология/симптомы → причины → решения

## 3.1. Снаружи сайт не открывался (ERR_CONNECTION_TIMED_OUT)

**Симптом:** `http://<IP>:8080` не отвечает.
**Причина:** порт **8080** был закрыт на **FW провайдера**.
**Решение:**

- Открыть 8080/TCP в панели провайдера (и/или в облачном сетевом ACL).
- Проверить UFW/iptables на самом сервере (если включены).
- Проверка: `curl http://127.0.0.1:8080/api/health` на сервере и из внешней сети браузером.

## 3.2. Контейнер backend перезапускался (SyntaxError)

**Симптом (логи):**

```
SyntaxError: trailing comma not allowed without surrounding parentheses
  File "/code/backend/app/schemas/__init__.py", line 3
    from .user import ..., Token,
```

**Причина:** запятая в импорте без обрамляющих скобок.
**Решение:** удалить хвостовую запятую, привести `__all__` к валидному списку.

## 3.3. Pydantic v2: “Config” и “model_config” вместе

**Симптом:**

```
pydantic.errors.PydanticUserError: "Config" and "model_config" cannot be used together
```

**Причина:** в `UserRead` одновременно использовались `class Config: orm_mode = True` и `model_config`.
**Решение:** оставить **только** pydantic v2 стиль:

```python
class UserRead(UserBase):
    id: int
    created_at: Optional[datetime] = None
    model_config = {"from_attributes": True}
```

## 3.4. 404 на `/health`

**Симптом:** `GET /health` → 404.
**Причина:** реальный путь — `/api/health` (префикс `api`).
**Решение:** использовать `GET /api/health`. Для самопроверки:

```bash
docker compose -f docker-compose.prod.yml exec backend \
  python -c "from backend.app.main import app; print([r.path for r in app.routes])"
```

## 3.5. Ошибки SQLAlchemy при создании пользователя

**Симптомы по очереди:**

```
TypeError: 'password' is an invalid keyword argument for User
TypeError: 'hashed_password' is an invalid keyword argument for User
```

**Причина:** в модели `User` поле называется **`password_hash`**, а в сервисе передавались `password`/`hashed_password`.
**Решение:** в `services/users.py` создавать модель так:

```python
new_user = models.User(
    username=user.username,
    email=user.email,
    role=user.role,          # по умолчанию у вас user
    password_hash=hashed_password,
)
```

## 3.6. Токен валиден, но `/api/auth/me` отвечал «Неверный или просроченный токен»

**Причина:** несогласованность между тем, что кладём в `sub` и тем, как это читаем.
**Решение (рабочий вариант):**

- На логине генерим токен с `sub = username`.
- В `get_current_user` читаем `sub` как **username** и ищем юзера по `username`.

После правок `/api/auth/me` начал возвращать:

```json
{
  "username": "alice",
  "email": "alice@example.com",
  "role": "user",
  "id": 1,
  "created_at": "2025-10-02T23:01:05.467984"
}
```

## 3.7. Сброс БД падал: “server is not running locally …”

**Причина:** мы вызывали `dropdb/createdb` сразу после `up db`, Postgres ещё не успевал подняться.
**Решение:** сначала запустить **только** БД, дождаться готовности (либо healthcheck, либо цикл ожидания), затем `dropdb/createdb`, потом — миграции.

# 4) Проверенные команды (cheat sheet)

## 4.1. Чистый подъём окружения

```bash
# Старт БД
docker compose -f docker-compose.prod.yml up -d db

# Подождать готовность БД (или сделать healthcheck/ожидание в Makefile)

# Применить миграции
docker compose -f docker-compose.prod.yml up -d backend
docker compose -f docker-compose.prod.yml exec backend alembic upgrade head

# Проверка API
curl http://127.0.0.1:8080/api/health   # {"status":"ok"}
```

## 4.2. Регистрация / Логин / Me (curl)

```bash
# Register
curl -X POST http://127.0.0.1:8080/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","email":"alice@example.com","password":"secret123"}'

# Login
TOKEN=$(curl -s -X POST http://127.0.0.1:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","password":"secret123"}' | jq -r .access_token)

echo $TOKEN

# Me
curl -H "Authorization: Bearer $TOKEN" http://127.0.0.1:8080/api/auth/me
```

## 4.3. Полезные диагностики

```bash
# Логи backend
docker compose -f docker-compose.prod.yml logs -f backend | tail -n 200

# Список маршрутов FastAPI
docker compose -f docker-compose.prod.yml exec backend \
  python -c "from backend.app.main import app; print([r.path for r in app.routes])"

# Консоль psql
docker exec -it legal-assistant-db psql -U admin -d legal_assistant_db -c "\dt"
```

# 5) Postman: как настроено и что проверено

## 5.1. Окружение

- `base_url`: `http://<ваш_IP>:8080`
- `access_token`: пусто (заполняется автоматически после логина)

## 5.2. Коллекция запросов

1. **POST** `{{base_url}}/api/auth/register`
   Body (JSON):

   ```json
   { "username": ��"apitest", "email": "test@example.com", "password": "123456" }
   ```

   Ожидаемые ответы:
   - `200` — создан пользователь;
   - `400 {"detail":"Username already registered"}` — если уже есть.

2. **POST** `{{base_url}}/api/auth/login`
   Body (JSON):

   ```json
   { "username": ��"apitest", "password": "123456" }
   ```

   В **Tests**:

   ```js
   pm.environment.set("access_token", pm.response.json().access_token);
   ```

3. **GET** `{{base_url}}/api/auth/me`
   **Authorization**: Bearer Token → `{{access_token}}`.
   Ответ: JSON с данными текущего пользователя.

## 5.3. Типичные статусы/ошибки

- `400 Username already registered` — регистрация дубля.
- `401 Invalid credentials` — не тот пароль.
- `401 Неверный или просроченный токен` — отсутствует/битый/просрочен JWT или не передан заголовок `Authorization: Bearer`.

# 6) Итоговое состояние кода (ключевые моменты)

- **models.User** содержит поле `password_hash` (обязательно), роли — через `ENUM(UserRole)`.
- **services/users.py**:
  - проверка уникальности `username` и `email`;
  - хеширование пароля `passlib` (bcrypt, обрезка до 72 байт);
  - создание пользователя с `password_hash=...`.

- **core/security.py**:
  - `create_access_token` кладёт `sub=username` и `exp`;
  - `get_current_user` читает `sub` как username и вытягивает пользователя из БД.

- **routes/auth.py**:
  - `/register` — создаёт пользователя, возвращает `UserRead`;
  - `/login` — проверяет пароль, возвращает `{"access_token", "token_type":"bearer"}`;
  - `/me` — защищённый эндпоинт, возвращает `UserRead` по токену.

# 7) Обновления Makefile (важные)

- **reset-all** разделён на шаги: сначала БД, затем миграции, потом backend; добавлено ожидание готовности БД (иначе `dropdb/createdb` могут упасть).
- Цели `health-host` и `health-container` помогают быстро проверить, жив ли API.
- Добавлены удобные цели `ps`, `logs`, `shell`, `db-shell`, `db-tables`, `seed`.

# 8) Рекомендации/дальнейшие шаги

1. **Refresh-токены** + короткий TTL для access-токена.
2. **Логаут** (чёрный список токенов или ротация ключа).
3. **Роли и доступы**: декоратор `Depends(role_required("admin"))` на админских маршрутах.
4. **Тесты**: pytest на register/login/me; цель `make test-auth`.
5. **Документация**: вынести Postman collection в JSON в репозиторий (`/docs/postman/legal-assistant.postman_collection.json`).
6. **Наблюдаемость**: базовый логинг запросов/исключений, метрики (при желании — Prometheus/Grafana).

---

Если хочешь, подготовлю готовый Postman JSON (коллекция + окружение), чтобы можно было просто импортировать и не настраивать вручную.
