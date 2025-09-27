Отличная идея 💡
Я подготовил для тебя отдельный файл `docs/LOCAL_DEV.md`, чтобы разработчики имели быстрый гайд именно по локальной разработке (без Docker).

---

## 📄 docs/LOCAL_DEV.md

````markdown
# 🛠 LOCAL DEV — Legal Assistant API v2

Руководство для локальной разработки без Docker.

---

## ⚙️ 1. Подготовка окружения

Установи зависимости:
```bash
sudo apt update
sudo apt install -y python3.12 python3.12-venv python3-pip git make
````

Клонируй проект:

```bash
cd ~/my_projects
git clone https://github.com/aw56/legal-assistant-arbitrage-v2.git
cd legal-assistant-arbitrage-v2
```

---

## 📦 2. Настройка окружения

Создай локальный `.env.local`:

```bash
nano .env.local
```

Пример:

```dotenv
POSTGRES_USER=admin
POSTGRES_PASSWORD=Admin@2025!
POSTGRES_DB=legal_assistant_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

SECRET_KEY=local_dev_secret
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

TEST_SQLITE=1
OPENAPI_JSON_PATH=docs/openapi.json
```

Активируй:

```bash
make env-local
```

---

## 🐍 3. Виртуальное окружение и зависимости

Создание окружения:

```bash
make venv
```

Установка зависимостей:

```bash
make deps
```

---

## ▶️ 4. Запуск API

Обычный запуск (foreground):

```bash
make run
```

Запуск в фоне:

```bash
make run-bg
```

Остановить фоновые процессы:

```bash
make stop
```

---

## 🧪 5. Тестирование

Запуск тестов с SQLite:

```bash
make test
```

---

## 📖 6. Документация API

Сгенерировать документацию:

```bash
make docs
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

ReDoc:

```
http://127.0.0.1:8000/redoc
```

---

## 🔧 7. Утилиты

* Освободить порт 8000:

  ```bash
  make kill-8000
  ```
* Освободить произвольный порт:

  ```bash
  make kill-port PORT=XXXX
  ```

---

## ✅ Итог

* Локальная разработка возможна без Docker.
* Управление сервисом упрощено через `Makefile`.
* Есть поддержка фонового запуска (`make run-bg`) и остановки (`make stop`).
* Тесты запускаются на SQLite, продакшен — на PostgreSQL.

```

---

Хочешь, я теперь соберу для тебя **связанный комплект документации**:  
- `README.v2.md` — основной обзор  
- `docs/DEPLOY.md` — продакшен  
- `docs/LOCAL_DEV.md` — локалка  
- `docs/TROUBLESHOOTING.md` — отладка  

Чтобы вся команда могла легко ориентироваться?
```

