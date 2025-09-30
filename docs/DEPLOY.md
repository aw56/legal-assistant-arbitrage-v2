Отлично 🙌 Давай сразу закроем вопрос с документацией, чтобы у тебя был **полный комплект**.
Я подготовлю два файла:

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
{"status":"ok","version":"0.1.0","env":"production","db":"connected"}
```

---

## 🔄 Миграции базы

```bash
make migrate
```

---

## 🛑 Остановка

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
* Подключить мониторинг: Prometheus + Grafana.
* Логи ошибок отправлять в Sentry.

````

---

# 📄 `docs/LOCAL_DEV.md`

```markdown
# 🛠 Локальная разработка Legal Assistant Arbitrage API (v2)

## 🔧 Установка окружения

Установи зависимости:

```bash
sudo apt update
sudo apt install -y python3.12-venv python3-pip git make
````

---

## 📦 Настройка проекта

### 1. Клонируем репозиторий

```bash
git clone git@github.com:aw56/legal-assistant-arbitrage-v2.git
cd legal-assistant-arbitrage-v2
```

### 2. Создаём виртуальное окружение

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## ⚙️ Настройка `.env`

Локально можно работать на **SQLite**.
В `.env` укажи:

```dotenv
USE_SQLITE=1
```

Для PostgreSQL (через Docker):

```dotenv
USE_SQLITE=0
POSTGRES_USER=admin
POSTGRES_PASSWORD=Admin@2025!
POSTGRES_DB=legal_assistant_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

---

## ▶️ Запуск API

### С SQLite (локально)

```bash
make run
```

Доступ:

* Swagger → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* Health → [http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health)

### С PostgreSQL (через Docker)

```bash
make docker
```

---

## 🗄️ Работа с миграциями

### Создать новую миграцию

```bash
make makemigrations
```

### Применить миграции

```bash
make migrate
```

---

## 🧪 Тесты

Тесты используют SQLite:

```bash
make test
```

---

## 🔨 Полезные команды (Makefile)

* `make run` — запуск API локально
* `make docker` — запуск через docker-compose (dev)
* `make docker-prod` — запуск продакшн окружения
* `make migrate` — применить миграции
* `make test` — запустить тесты
* `make health-host` — проверить API с хоста
* `make shell` — войти в контейнер backend

---

## 🛠 Лайфхаки

* Автодополнение запросов → Swagger UI.
* При изменении моделей → обязательно создавай миграции.
* Для изоляции зависимостей → держи `venv` активированным.

```

---

📌 Теперь у тебя:
- `README.md` — паспорт проекта.
- `docs/DEPLOY.md` — деплой на сервер.
- `docs/LOCAL_DEV.md` — разработка локально.
- `docs/TROUBLESHOOTING.md` — отладка.
- `docs/GIT_SETUP.md` — работа с Git.

---

Хочешь, я ещё дополню `docs/TROUBLESHOOTING.md`, чтобы там были все типовые ошибки, которые у нас уже встречались (psycopg2, alembic, docker, env)?
```
