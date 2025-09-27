Отлично 🙌
Я вынесу расширенный раздел **Troubleshooting** в отдельный файл `docs/TROUBLESHOOTING.md`, чтобы разработчикам было удобно открывать его отдельно, а в README останется только ссылка.

---

## 📄 docs/TROUBLESHOOTING.md

```markdown
# 🧨 Troubleshooting — Legal Assistant API v2

Собраны типовые ошибки и их решения при работе с проектом.

---

## 🔹 Адрес уже занят (port 8000)

**Симптом:**  
```

ERROR: [Errno 98] Address already in use

````

**Причина:**  
Порт `8000` занят другим процессом (старый uvicorn или контейнер).

**Решение:**  
```bash
make kill-8000
````

или для любого порта:

```bash
make kill-port PORT=XXXX
```

---

## 🔹 Контейнер backend перезапускается

**Причины:**

* неправильный пароль/хост БД
* база ещё не готова

**Решение:**

* проверь `.env.prod` (пароль без спецсимволов)
* убедись, что `POSTGRES_HOST=db`
* дождись готовности БД (скрипт `wait-for-db.sh` проверяет через SQLAlchemy)

---

## 🔹 Ошибки с паролем `Admin@2025!`

**Симптом:**

```
database "admin" does not exist
```

**Причина:**
В Docker строка подключения ломается из-за спецсимволов в пароле.

**Решение:**

* Для Docker используй пароль **без спецсимволов** (например, `Admin2025`)
* Для локальной разработки можно оставить сложный пароль (`Admin@2025!`)

---

## 🔹 Миграции не применяются

**Симптом:**
Ошибка подключения или отсутствуют таблицы.

**Решение:**
Применить миграции вручную:

```bash
docker exec -it legal-assistant-arbitrage-v2-backend-1 alembic upgrade head
```

---

## 🔹 SQLite vs PostgreSQL

**Симптом:**

```
sqlite3.OperationalError: no such table
```

**Причина:**
SQLite база пустая (тестовый режим).

**Решение:**

* Убедись, что `TEST_SQLITE=1` для тестов
* В `conftest.py` есть `Base.metadata.create_all()`

---

## 🔹 Docker: контейнеры не стартуют

**Симптом:**
`Error response from daemon: failed to bind host port ... address already in use`

**Причина:**
Порт уже занят другим процессом/контейнером.

**Решение:**

1. Остановить контейнеры:

   ```bash
   make docker-prod-down
   ```
2. Проверить процессы:

   ```bash
   make kill-port PORT=8080
   ```
3. Перезапустить:

   ```bash
   make docker-prod-restart
   ```

---

## 🔹 Проверка состояния

* Логи backend:

  ```bash
  docker logs -f legal-assistant-arbitrage-v2-backend-1
  ```
* Логи базы:

  ```bash
  docker logs -f legal-assistant-arbitrage-v2-db-1
  ```
* Проверка healthcheck:

  ```bash
  curl http://127.0.0.1:8080/health
  ```

---

````

---

## 📌 В README останется ссылка:

В секции **Troubleshooting** можно будет оставить только:

```markdown
## 🧨 Troubleshooting

Раздел вынесен в отдельный файл 👉 [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)
````

---

Хочешь, я ещё подготовлю `docs/DEPLOY.md`, где будет подробно описано, как запускать проект **на сервере в продакшене** (шаги: установка Docker, make env-prod, make docker-prod)?
