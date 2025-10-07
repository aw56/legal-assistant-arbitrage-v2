Отличная идея 💡 — я сделаю для тебя **полный `docs/COMMANDS.md`**, где будут:

1. Все команды из Makefile (с описанием и примерами).
2. Логика их взаимодействия между собой (цепочки и сценарии).
3. Карта модулей (auth, users, laws, decisions, migrations, тесты) и какие команды с ними связаны.

---

# ⚖️ Legal Assistant Arbitrage v2 — Makefile & Commands

## 🔎 Обзор

Makefile — это центральная точка управления проектом. Он связывает:

* **Docker** (запуск/остановка контейнеров, логи, shell);
* **Базу данных (PostgreSQL + Alembic)** (миграции, ресет, дампы);
* **FastAPI** (локальный запуск, проверка API, smoke-тесты);
* **CI/CD** (линтеры, тесты, автодеплой);
* **Git** (commit, push, sync).

---

## 📂 Основные категории команд

### 🐳 Docker

* `make up` — запустить контейнеры.
* `make down` — остановить контейнеры.
* `make rebuild` — пересобрать проект (удаляет volume).
* `make ps` — список контейнеров.
* `make logs` — логи backend + db.
* `make shell` — открыть Bash внутри backend.

**Взаимосвязь:**
Все остальные команды (миграции, тесты, сиды) работают только после `make up`.

---

### 🗄️ Alembic / Миграции

* `make migrate` — применить все миграции.
* `make makemigrations` — создать новую миграцию.
* `make reset-db` — пересоздать БД и накатить миграции.
* `make reset-migrations` — снести миграции и создать init.
* `make current` — текущая версия миграции.
* `make history` — история миграций.
* `make downgrade v=-1` — откатить миграции.
* `make stamp-head` — пометить миграции как применённые.
* `make fix-migrations` — автофикс Alembic.

**Взаимосвязь:**

* `reset-db` зависит от **db** контейнера.
* После `makemigrations` всегда делаем `migrate`.
* `seed` можно запускать после `migrate` (загрузка данных).

---

### 🐘 PostgreSQL

* `make db-shell` — консоль psql.
* `make db-tables` — список таблиц.
* `make db-dump` — сохранить дамп БД.
* `make db-restore` — восстановить из дампа.
* `make db-reset-tables` — очистить все таблицы.
* `make drop-db` — удалить базу.
* `make check-db` — проверить соединение с БД.

**Взаимосвязь:**

* `reset-db` вызывает `drop-db` и `createdb`.
* `db-inspect` помогает синхронизировать миграции и структуру.

---

### ❤️ Healthcheck & Smoke

* `make health-host` — проверка API снаружи (127.0.0.1:8080).
* `make health-container` — проверка API изнутри контейнера (порт 8000).
* `make smoke` — smoke-тесты.
* `make routes` — список всех маршрутов FastAPI.

**Взаимосвязь:**

* Используются после `up` и `migrate`.
* `smoke` проверяет auth + laws + decisions CRUD.

---

### ✅ Тесты

* `make test` — запустить pytest.
* `make test-verbose` — тесты в подробном режиме.
* `make docker-test` — тесты в контейнере.
* `make ci-test` — тесты для CI (pytest + API).
* `make coverage` — покрытие тестами.

**Интеграционные тесты API:**

* `make test-auth` — register/login/me.
* `make test-laws` — CRUD для laws.
* `make test-decisions` — CRUD для decisions.
* `make test-api` — полный цикл (auth + laws + decisions).

---

### 🔧 Git

* `make git-add` — добавить изменения.
* `make git-commit m="msg"` — commit.
* `make git-push` — push.
* `make git-all` — add+commit+push.
* `make git-sync` — подтянуть origin/main.
* `make git-reset-hard` — жёсткий сброс.
* `make git-amend` — amend последнего коммита.

---

### 🚀 FastAPI локально

* `make run` — запуск uvicorn локально.
* `make stop` — остановка uvicorn.
* `make restart` — перезапуск.
* `make logs-local` — логи uvicorn.

---

### 📖 Документация

* `make apidocs` — генерация API_DOCS.md.
* `make archdocs` — генерация ARCHITECTURE.md.
* `make docs` — полная генерация документации.

---

### 🤖 CI/CD

* `make ci-lint` — линтеры.
* `make ci-build` — проверка сборки.
* `make ci-deploy` — деплой через CI/CD.
* `make deploy` — локальный деплой (setup-prod).

---

## 🔗 Логика взаимодействия инструментов

1. **Dev цикл:**

   ```bash
   make up
   make migrate
   make seed
   make health-host
   make test-api
   ```

   🔹 Запускает контейнеры → накатывает миграции → заливает сиды → проверяет API → гоняет интеграционные тесты.

2. **Prod цикл:**

   ```bash
   make rebuild
   make migrate
   make seed
   make health-host
   make deploy
   ```

   🔹 Полный деплой с нуля.

3. **CI/CD:**

   * `make ci-lint`
   * `make ci-test`
   * `make ci-deploy`

---

## 🗺️ Карта модулей и команд

* **auth** → тестируется `test-auth`, участвует в smoke-тестах.
* **users** → связаны с auth, но CRUD покрывается в API-тестах.
* **laws** → `test-laws`.
* **decisions** → `test-decisions`.
* **migrations** → `migrate`, `reset-db`, `makemigrations`.
* **db** → `db-shell`, `db-tables`, `db-dump`.
* **docs** → `apidocs`, `archdocs`.

---

👉 Таким образом, `Makefile` — это glue code, который объединяет:

* Docker (infra)
* Alembic (migrations)
* FastAPI (API)* pytest (tests)
* Git (workflow)
* Docs (генерация)

---

## 🖼️ Диаграмма связей (Makefile ↔︎ модули проекта)

```mermaid
flowchart TD
    subgraph Docker/Infra
        UP[make up] --> MIGRATE
        REBUILD[make rebuild] --> MIGRATE
        DOWN[make down]
        LOGS[make logs]
    end

    subgraph DB
        MIGRATE[make migrate] --> DB[(PostgreSQL)]
        RESETDB[make reset-db] --> DB
        RESETMIG[make reset-migrations] --> DB
        DBTABLES[make db-tables] --> DB
        DBDUMP[make db-dump] --> DB
        DBRESTORE[make db-restore] --> DB
        DBRESETTABLES[make db-reset-tables] --> DB
        DROPDB[make drop-db] --> DB
    end

    subgraph API (FastAPI)
        HEALTH[make health-host] --> ROUTES[make routes]
        SMOKE[make smoke] --> APIROUTES
        TESTAPI[make test-api] --> APIROUTES
        APIROUTES[/routes: auth, users, laws, decisions/]
    end

    subgraph Tests
        TEST[make test]
        TESTV[make test-verbose]
        DOCKTEST[make docker-test]
        CITEST[make ci-test]
        TESTAUTH[make test-auth] --> APIROUTES
        TESTLAWS[make test-laws] --> APIROUTES
        TESTDEC[make test-decisions] --> APIROUTES
        TESTAPI --> TESTAUTH & TESTLAWS & TESTDEC
    end

    subgraph Docs
        APIDOCS[make apidocs] --> API_DOCS
        ARCHDOCS[make archdocs] --> ARCHITECTURE
        DOCS[make docs] --> APIDOCS & ARCHDOCS
    end

    subgraph Git
        GITADD[make git-add]
        GITCOMMIT[make git-commit]
        GITPUSH[make git-push]
        GITALL[make git-all] --> GITADD & GITCOMMIT & GITPUSH
        GITSYNC[make git-sync]
        GITRESET[make git-reset-hard]
    end

    subgraph Local FastAPI
        RUN[make run] --> FASTAPI
        STOP[make stop] -.-> FASTAPI
        RESTART[make restart] --> FASTAPI
        STATUS[make status]
        LOGSLOCAL[make logs-local]
        FASTAPI[(Uvicorn Local)]
    end

    subgraph CI/CD
        CILINT[make ci-lint] --> LINTERS
        CIBUILD[make ci-build] --> BUILD
        CIDEPLY[make ci-deploy] --> DEPLOY
        DEPLOY[make deploy] --> SETUPPROD
        SETUPPROD[make setup-prod] --> UP
    end
```

---

## 🔎 Как читать диаграмму

* **Docker-блок** управляет окружением (контейнеры).
* **DB-блок** отвечает за PostgreSQL и миграции Alembic.
* **API-блок** (FastAPI) — это маршруты `/api/*`, которые тестируются.
* **Tests-блок** проверяет API и бизнес-логику.
* **Docs-блок** генерирует API_DOCS и ARCHITECTURE.
* **Git-блок** управляет репозиторием.
* **Local FastAPI** позволяет запускать проект без Docker.
* **CI/CD** связывает всё через пайплайны.
---

👉 Таким образом, у тебя теперь есть **полный справочник по Makefile** + **визуальная карта команд и модулей**.
