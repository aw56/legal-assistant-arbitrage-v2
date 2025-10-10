Отлично 🚀
Тогда давай сделаем так: я соберу для тебя **полный `README.md`**, а ты сможешь сразу положить его в проект (`legal-assistant-arbitrage-v2/README.md`).

Вот готовое содержимое:

---

````markdown
# ⚖️ Legal Assistant Arbitrage v2

Добро пожаловать!
Этот проект использует **FastAPI + PostgreSQL + Docker + Alembic**.
Все основные команды собраны в `Makefile`.

---

## 🚀 Быстрый старт

### Dev-окружение

```bash
make init-dev
```
````

👉 Устанавливает зависимости, поднимает контейнеры, применяет миграции, загружает сиды и запускает тесты.

### Prod-окружение

```bash
make up
```

👉 Поднимает контейнеры и запускает API.

---

## 🐳 Docker

| Команда               | Описание                 |
| --------------------- | ------------------------ |
| `make up`             | Запуск контейнеров       |
| `make down`           | Остановка контейнеров    |
| `make rebuild`        | Пересоздать контейнеры   |
| `make restart-docker` | Перезапустить контейнеры |
| `make logs`           | Логи всех сервисов       |
| `make ps`             | Список контейнеров       |
| `make shell`          | Bash внутри backend      |

---

## 🗄️ База данных (PostgreSQL)

| Команда                      | Описание                                |
| ---------------------------- | --------------------------------------- |
| `make db-shell`              | Подключиться к БД (psql)                |
| `make db-tables`             | Список таблиц                           |
| `make db-dump`               | Сделать дамп БД                         |
| `make db-restore`            | Восстановить из дампа                   |
| `make db-reset-tables`       | Очистить все таблицы                    |
| `make db-drop-table t=users` | Удалить таблицу users                   |
| `make seed`                  | Загрузить сиды из `seeds/init_data.sql` |

---

## 🔀 Alembic (миграции)

| Команда               | Описание                            |
| --------------------- | ----------------------------------- |
| `make makemigrations` | Создать новую миграцию              |
| `make migrate`        | Применить все миграции              |
| `make current`        | Показать текущую миграцию           |
| `make history`        | История миграций                    |
| `make heads`          | Показать все head-миграции          |
| `make downgrade v=-1` | Откатить на 1 миграцию назад        |
| `make merge-heads`    | Слить несколько heads               |
| `make stamp-head`     | Отметить миграции как применённые   |
| `make reset-db`       | Пересоздать БД и применить миграции |

---

## 🚀 FastAPI (локально)

| Команда           | Описание                 |
| ----------------- | ------------------------ |
| `make run`        | Запуск FastAPI (uvicorn) |
| `make stop`       | Остановить FastAPI       |
| `make status`     | Проверить статус uvicorn |
| `make logs-local` | Логи uvicorn             |
| `make restart`    | Перезапуск uvicorn       |

---

## ❤️ Healthcheck

| Команда                 | Описание                              |
| ----------------------- | ------------------------------------- |
| `make health-host`      | Проверка API с хоста (127.0.0.1:8080) |
| `make health-container` | Проверка API из контейнера            |

---

## 🔧 Git

| Команда                     | Описание                           |
| --------------------------- | ---------------------------------- |
| `make git-add`              | Добавить изменения                 |
| `make git-fix`              | Авто-фиксы (pre-commit + миграции) |
| `make git-commit m="fix:x"` | Commit                             |
| `make git-push`             | Push                               |
| `make git-all m="feat:x"`   | add + fix + commit + push          |
| `make git-amend`            | Amend последнего коммита           |
| `make git-sync`             | Sync с origin/main                 |
| `make git-reset-hard`       | Полный сброс до origin/main        |
| `make git-reset-soft`       | Soft reset (сохраняем изменения)   |

---

## ✅ Тесты

| Команда             | Описание                  |
| ------------------- | ------------------------- |
| `make test`         | Запуск тестов             |
| `make test-verbose` | Подробный запуск тестов   |
| `make docker-test`  | Запуск всех тестов        |
| `make ci-test`      | Тесты в CI/CD             |
| `make coverage`     | Отчёт по покрытию тестами |

---

## 📖 Документация

| Команда        | Описание                               |
| -------------- | -------------------------------------- |
| `make apidocs` | Сгенерировать `API_DOCS.md` из OpenAPI |

---

## 🔥 Полезные сценарии

- **Полный ресет проекта (с чистой БД):**

  ```bash
  make reset-db
  ```

- **Удалить все таблицы БД:**

  ```bash
  make db-reset-tables
  ```

- **Проверить API после запуска:**

  ```bash
  make health-host
  ```

---

💡 Совет: для ежедневной работы чаще всего нужны команды
`make up`, `make logs`, `make db-shell`, `make migrate`, `make test`, `make git-all`.

---

```

---

Хочешь, я прямо сейчас создам файл `README.md` в проекте с этим содержимым?
```
