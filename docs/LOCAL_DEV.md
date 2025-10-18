---

````markdown
# 🛠 Локальная разработка — Legal Assistant Arbitrage v2.9.7

## 📦 1. Подготовка окружения

### 1.1 Установка зависимостей

```bash
sudo apt update
sudo apt install -y python3.12-venv python3-pip git make
````

### 1.2 (Опционально) Docker и Compose

```bash
sudo apt install -y docker.io docker-compose-plugin
sudo usermod -aG docker $USER
newgrp docker
```

---

## 🔐 2. Настройка окружения

Скопируй шаблон `.env.example` → `.env`:

```bash
cp .env.example .env
```

Для локальной разработки используется **SQLite**.
Добавь в `.env`:

```dotenv
USE_SQLITE=1
```

Если ты хочешь использовать PostgreSQL (Docker/Prod), установи:

```dotenv
USE_SQLITE=0
```

---

## ▶️ 3. Запуск приложения

Локальный сервер:

```bash
make run
```

Приложение будет доступно по адресам:

- **Swagger UI** → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Healthcheck** → [http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health)

---

## 🧪 4. Тестирование

Все тесты по умолчанию используют SQLite (in-memory).
Запуск тестов:

```bash
make test
```

Если нужно протестировать через PostgreSQL, включи Docker и выполни:

```bash
make docker
make test
```

---

## 🗄️ 5. Работа с базой данных

### 5.1 SQLite (по умолчанию)

Файл базы создаётся локально → `test.db`

Проверить таблицы:

```bash
sqlite3 test.db ".tables"
```

### 5.2 PostgreSQL (через Docker)

1. Поднять контейнеры:

   ```bash
   make docker
   ```

2. Применить миграции:

   ```bash
   alembic upgrade head
   ```

3. Проверить соединение:

   ```bash
   docker exec -it legal-assistant-db psql -U postgres -d legal_assistant
   ```

---

## 🧩 6. Управление миграциями

Создать новую миграцию:

```bash
alembic revision --autogenerate -m "add new field to laws"
```

Применить миграции:

```bash
alembic upgrade head
```

Откатить последнюю миграцию:

```bash
alembic downgrade -1
```

---

## 🧨 7. Troubleshooting

### 7.1 Ошибка: порт 8000 занят

```bash
lsof -i :8000
kill -9 <PID>
```

### 7.2 SQLite база не обновляется

Удалить файл `test.db` и перезапустить сервер:

```bash
rm test.db
make run
```

### 7.3 Docker не запускается

Проверь состояние службы:

```bash
sudo systemctl status docker
sudo systemctl restart docker
```

---

## 🧭 8. Полезные команды Makefile

| Команда              | Назначение                          |
| -------------------- | ----------------------------------- |
| `make run`           | Запуск FastAPI локально             |
| `make test`          | Запуск всех тестов                  |
| `make docker`        | Поднятие контейнеров                |
| `make check-all`     | Полная проверка кода и документации |
| `make progress-auto` | Автоматический снапшот прогресса    |
| `make weekly-check`  | Еженедельная DevOps-проверка        |

---

## 📘 9. Полезные ссылки

- [docs/DEVOPS_PRACTICE_GUIDE.md](./DEVOPS_PRACTICE_GUIDE.md)
- [docs/CI_PIPELINE_GUIDE.md](./CI_PIPELINE_GUIDE.md)
- [docs/SAFE_PUSH_AND_VERIFICATION_GUIDE_v2.8.md](./SAFE_PUSH_AND_VERIFICATION_GUIDE_v2.8.md)

---

📅 Последняя ревизия: 2025-10-16
👤 Автор: **Aleksej (Project Owner)**
🔖 Версия: **v2.9.7 LTS**

```

---
```
