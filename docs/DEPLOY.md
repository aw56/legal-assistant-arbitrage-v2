Отлично 🙌
Я подготовлю тебе **полные финализированные версии** двух файлов:

* `docs/DEPLOY.md` — только про деплой (подготовка сервера, запуск, миграции, мониторинг).
* `docs/TROUBLESHOOTING.md` — каталог ошибок и решений.

Они будут независимые и полные (без сокращений).

---

# 📄 `docs/DEPLOY.md`

````markdown
# 🚀 Деплой Legal Assistant Arbitrage API (v2)

## 🔧 Подготовка сервера

Установи зависимости:

```bash
sudo apt update
sudo apt install -y python3-pip python3.12-venv git make docker.io docker-compose-plugin
````

Проверь версии:

```bash
docker --version
docker compose version
python3 --version
```

---

## 📦 Развёртывание проекта

### 1. Клонируем репозиторий

```bash
git clone git@github.com:aw56/legal-assistant-arbitrage-v2.git
cd legal-assistant-arbitrage-v2
```

### 2. Настраиваем окружение

Скопируй `.env.example` → `.env` и отредактируй:

```bash
cp .env.example .env
nano .env
```

Параметры по умолчанию:

```dotenv
POSTGRES_USER=admin
POSTGRES_PASSWORD=Admin@2025!
POSTGRES_DB=legal_assistant_db
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

---

### 3. Запуск в **production-режиме**

```bash
make rebuild
```

Проверка API:

```bash
make health-host
```

Ожидаемый ответ:

```json
{
  "status":"ok",
  "version":"0.1.0",
  "env":"production",
  "db_status":"connected",
  "alembic":"up-to-date"
}
```

---

## 🔄 Миграции базы

Применить все миграции:

```bash
make migrate
```

Создать новую миграцию:

```bash
make makemigrations
```

---

## ⚡ Сброс базы данных

Полностью удалить данные и пересоздать схему:

```bash
make reset-db
```

---

## 🛑 Остановка контейнеров

```bash
make down
```

---

## 📊 Мониторинг

* Логи backend:

  ```bash
  make logs
  ```

* Проверка состояния контейнеров:

  ```bash
  make ps
  ```

---

## 🛡 Рекомендации для продакшена

* Использовать **реверс-прокси** (Nginx/Traefik) с HTTPS.
* Настроить **systemd unit** для автозапуска `docker compose`.
* Подключить мониторинг: **Prometheus + Grafana**.
* Ошибки отправлять в **Sentry**.
* Резервные копии БД делать с помощью `pg_dump`.

````

---
