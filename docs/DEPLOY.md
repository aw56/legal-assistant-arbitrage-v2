# 📄 `docs/DEPLOY.md`

````markdown
# 🚀 Деплой Legal Assistant Arbitrage API (v2)

## 🔧 Подготовка сервера

Установи зависимости:

```bash
sudo apt update
sudo apt install -y python3-pip python3.12-venv git make docker.io docker-compose-plugin
```
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

Отлично, Алексей 👌

<!-- markdownlint-disable MD013 -->

Вот полностью обновлённый и профессионально оформленный **`docs/DEPLOY.md`** — версия `v2.5`, адаптированная под твою актуальную архитектуру (Docker + Makefile + CI/CD pipeline).

<!-- markdownlint-disable MD013 -->

Файл самодостаточный, с практическими командами, health-check’ами и интеграцией в AutoAuth-пайплайн.

---

````markdown
# 🚀 Деплой Legal Assistant Arbitrage API — v2.5

**Версия документа:** 2.5
**Обновлено:** 2025-10-13
**Автор:** Alex (admin@legal-assistant)

---

## ⚙️ 1. Подготовка окружения

Для развёртывания требуются:

- Ubuntu 22.04+ (или совместимая система)
- Docker + Compose plugin
- Python 3.12 (для локальной сборки)
- Make 4.3+

Установка зависимостей:

```bash
sudo apt update
sudo apt install -y python3.12-venv python3-pip git make docker.io docker-compose-plugin
```
````

Проверка версий:

```bash
docker --version
docker compose version
python3 --version
```

---

## 📦 2. Клонирование проекта

```bash
git clone git@github.com:aw56/legal-assistant-arbitrage-v2.git
cd legal-assistant-arbitrage-v2
```

---

## 🔐 3. Настройка переменных окружения

Скопируй пример `.env` и отредактируй:

```bash
cp .env.example .env
nano .env
```

Пример базовой конфигурации:

```dotenv
POSTGRES_USER=admin
POSTGRES_PASSWORD=Admin@2025!
POSTGRES_DB=legal_assistant_db
POSTGRES_HOST=db
POSTGRES_PORT=5432

TELEGRAM_TOKEN=xxxxx
SENTRY_DSN=
ENV=production
```

---

## 🧱 4. Запуск приложения (production)

Полный деплой (с пересборкой образа, миграциями и health-check):

```bash
make rebuild
```

Ожидаемый результат:

```bash
docker compose ps
```

```
NAME                  STATUS          PORTS
legal-assistant-db    Up (healthy)    0.0.0.0:5432->5432/tcp
legal-assistant-api   Up (healthy)    0.0.0.0:8080->8000/tcp
```

---

## 🩺 5. Проверка состояния API

Проверка через Makefile:

```bash
make health-host
```

или напрямую:

```bash
curl -f http://127.0.0.1:8080/api/health
```

Ответ:

```json
{ "status": "ok" }
```

Если контейнер перезапускается, смотри логи:

```bash
make logs
```

---

## 🧩 6. Управление миграциями базы

Применить все миграции:

```bash
make migrate
```

Создать новую миграцию:

```bash
make makemigrations
```

Полный сброс (drop → create → migrate):

```bash
make reset-db
```

или вручную:

```bash
docker exec -it legal-assistant-db psql -U admin -d postgres \
<!-- markdownlint-disable MD013 -->
  -c "DROP DATABASE IF EXISTS legal_assistant_db; CREATE DATABASE legal_assistant_db;"
<!-- markdownlint-disable MD013 -->
```

---

## 🧭 7. Основные команды Makefile

| Команда                 | Описание                        |
| ----------------------- | ------------------------------- |
| `make up`               | запуск контейнеров              |
| `make down`             | остановка контейнеров           |
| `make logs`             | просмотр логов backend          |
| `make ps`               | список контейнеров              |
| `make rebuild`          | пересборка образа и деплой      |
| `make snapshot-patches` | создание патчей и снапшотов     |
| `make weekly-check`     | автоматический аудит по cron    |
| `make telegram-test`    | тестовое уведомление в Telegram |

---

## 🔍 8. Health-checks и мониторинг

Docker автоматически проверяет:

- **PostgreSQL** — через `pg_isready`
- **Backend API** — через `/api/health`

Проверка из контейнера:

```bash
make health-container
```

Ожидаемый ответ:

```json
{
  "status": "ok",
  "version": "2.5",
  "env": "production",
  "db_status": "connected"
}
```

---

## 🧠 9. CI/CD Pipeline Integration (GitHub Actions)

CI/CD пайплайн версии v3.4 выполняет следующие шаги:

1. **Build & Lint** — проверка кода (`flake8`, `isort`, `black`, `markdownlint`).
2. **Test Suite** — `pytest + newman` (AutoAuth v3.4).
3. **Docker build** — сборка и прогон health-check внутри контейнера.
4. **Deploy** — деплой на staging или production-сервер.
5. **Notify** — отчёт в Telegram через `notify_telegram.py`.

Фрагмент YAML:

```yaml
- name: Run Docker health check
  run: |
    docker compose up -d
    sleep 10
    curl -f http://127.0.0.1:8080/api/health
```

---

## 🧾 10. Резервное копирование и восстановление

### 📤 Бэкап БД

```bash
docker exec -t legal-assistant-db pg_dump -U admin legal_assistant_db > backup_$(date +%F).sql
```

### 📥 Восстановление

```bash
cat backup_2025-10-13.sql | docker exec -i legal-assistant-db psql -U admin -d legal_assistant_db
```

---

## 🛡 11. Рекомендации для продакшена

- Использовать `restart: unless-stopped`
- Настроить реверс-прокси (Nginx/Traefik) с HTTPS:

  ```bash
  docker run -d -p 80:80 -p 443:443 --name nginx-proxy nginx
  ```

- Подключить мониторинг: Prometheus + Grafana
- Настроить Sentry через переменные `.env`
- Делать автоматические снапшоты:

  ```bash
  make snapshot-patches
  ```

---

## 🧩 12. Проверка перед релизом

Перед тегированием релиза `v2.5.0` убедись, что:

| Проверка  | Команда                 | Ожидаемый результат |
| --------- | ----------------------- | ------------------- |
| API жив   | `make health-host`      | `{"status":"ok"}`   |
| CI прошёл | `make test-ci-v3`       | Все тесты ✅        |
| Линтеры   | `make check-all`        | Без ошибок          |
| Патчи     | `make snapshot-patches` | Снапшот создан      |
| Telegram  | `make telegram-test`    | Уведомление пришло  |

---

## 🧭 13. Полный цикл деплоя

```bash
make down
git pull origin main
make rebuild
make migrate
make health-host
```

Ожидаемый результат:

```json
{ "status": "ok", "version": "2.5", "env": "production" }
```

---

💬 _“Automate what you fear, document what you trust.”_
— Alex, DevOps Lead, _Legal Assistant Arbitrage v2.5_

```

---

```
