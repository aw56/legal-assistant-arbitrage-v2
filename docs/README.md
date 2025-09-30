Отлично, у тебя уже есть хороший README, но давай сделаем **полностью финальную версию**, чтобы:

* проект был описан **от логики до реализации** (снизу вверх, как ты хочешь),
* все модули, зависимости и сервисы были связаны в единую картину,
* документация могла служить как **паспорт проекта для команды** и как **onboarding для нового разработчика**.

---

# 📘 Legal Assistant Arbitrage API — v2

Проект: **цифровой помощник юриста по арбитражным делам**
Стек: **Python 3.12 · FastAPI · SQLAlchemy 2 · Pydantic v2 · Alembic · PostgreSQL (prod) · SQLite (tests) · Docker · Makefile**

---

## 🔭 Цели проекта

1. Сформировать **материальную и процессуальную базу** (нормы + судебная практика).
2. Организовать **регулярную актуализацию** правовой информации.
3. Стандартизировать **клиентский запрос** (форма обращения).
4. Выполнять **правовой анализ** на основе базы (иерархия норм и практики).
5. Подсвечивать **коллизии** и предлагать их разрешение.
6. Формировать **мотивированное решение** с ссылками на нормы и практику.
7. Рассчитывать **шансы на успех (%)** по релевантной практике.
8. Учитывать **субъективные предпосылки** обращения в суд.
9. Предоставлять **шаблоны процессуальных документов**.
10. Обеспечить **автономность и локализацию** помощника.
11. Добавить **финансовый калькулятор** (госпошлина, региональные коэффициенты).
12. Подготовить **маркетинговую стратегию** по продвижению арбитражных дел.

---

## 🧭 Архитектурные принципы

* **Снизу вверх** (база → миграции → модели → бизнес-логика → API → CI/CD).
* **Разделение слоёв**:

  * **БД**: PostgreSQL (prod/dev), SQLite (тесты).
  * **ORM**: SQLAlchemy + миграции через Alembic.
  * **Модели**: SQLAlchemy ORM-модели (`models.py`).
  * **Схемы**: Pydantic v2 (`schemas/`).
  * **Бизнес-логика**: сервисы (`services/`).
  * **API**: FastAPI роуты (`routes/`).
* **Безопасность по умолчанию**: конфигурация через `.env`, пароли экранируются, в коде не хранятся.
* **Контейнеризация**: Docker + docker-compose для dev/prod.
* **Автоматизация**: Makefile для команд разработки.
* **CI/CD**: тесты, линтеры, автогенерация OpenAPI, деплой через Docker.

---

## 📁 Структура проекта

```bash
legal-assistant-arbitrage-v2/
├── backend/
│   ├── alembic/              # Миграции Alembic
│   └── app/
│       ├── database.py       # Подключение к БД (Postgres/SQLite)
│       ├── main.py           # Точка входа FastAPI
│       ├── models.py         # SQLAlchemy ORM-модели
│       ├── routes/           # API-роуты (health, users, laws, decisions)
│       ├── schemas/          # Pydantic-схемы
│       ├── services/         # Бизнес-логика (TODO)
│       └── tests/            # Тесты (pytest, SQLite)
├── docker-compose.yml         # Dev окружение
├── docker-compose.prod.yml    # Prod окружение
├── Dockerfile                 # Сборка backend
├── Makefile                   # Удобные команды
├── alembic.ini                # Конфигурация Alembic
├── requirements.txt           # Python-зависимости
├── wait-for-db.sh             # Скрипт ожидания БД
├── entrypoint.sh              # Точка запуска контейнера
├── docs/                      # Документация
│   ├── README.md
│   ├── DEPLOY.md
│   ├── LOCAL_DEV.md
│   ├── TROUBLESHOOTING.md
│   └── GIT_SETUP.md
└── .env.example               # Пример конфигурации
```

---

## ⚙️ Модули и библиотеки (логика снизу вверх)

### 1. **База данных**

* **PostgreSQL** (основная в prod/dev).
* **SQLite** (fallback для локальных тестов).
* Контейнеризация: Postgres запускается в `docker-compose.prod.yml`.

### 2. **SQLAlchemy ORM**

* `backend/app/models.py` — декларативные ORM-модели (users, laws, decisions).
* `backend/app/database.py` — подключение к БД, движок и сессия.

### 3. **Alembic**

* Управление миграциями.
* `alembic.ini` + `migrations/env.py` собирают строку подключения из `.env`.

### 4. **Pydantic v2**

* Строгая валидация входящих/исходящих данных.
* `schemas/` → определение API-контрактов (`UserCreate`, `LawResponse`, `DecisionInDB`).

### 5. **FastAPI**

* `main.py` инициализирует приложение.
* `routes/` → CRUD API (`/api/users`, `/api/laws`, `/api/decisions`).
* `/api/health` → health-check + проверка соединения с БД.

### 6. **Бизнес-логика (services/)**

* Вынесение логики из `routes/` в сервисы (чистые функции).
* Позволяет легко писать unit-тесты.

### 7. **CI/CD**

* GitHub Actions (pytest + lint + автодоки).
* Автогенерация `docs/API_DOCS.md` из OpenAPI.
* Деплой через `docker-compose.prod.yml`.

---

## 🔐 Конфигурация

`.env` (пример):

```dotenv
POSTGRES_USER=admin
POSTGRES_PASSWORD=Admin@2025!
POSTGRES_DB=legal_assistant_db
POSTGRES_HOST=db
POSTGRES_PORT=5432
USE_SQLITE=0
SECRET_KEY=super_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## ▶️ Запуск

### Локально

```bash
make run
```

Swagger: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
Health: [http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health)

### В Docker (prod)

```bash
make rebuild
make health-host
```

---

## 🗄️ Миграции

```bash
make migrate
make makemigrations
```

---

## 🧪 Тесты

```bash
make test
```

---

## 🔨 Makefile

```makefile
up             # Запуск контейнеров (dev/prod)
down           # Остановка контейнеров
rebuild        # Пересборка и перезапуск контейнеров
logs           # Просмотр логов
ps             # Список контейнеров
migrate        # Применить миграции
makemigrations # Создать новую миграцию
health-host    # Проверить health API с хоста
health-container # Проверить health API из контейнера
```

---

## 🧨 Troubleshooting

* ❌ **БД недоступна** → проверь `.env` и сеть docker.
* ❌ **Миграции падают** → удали volume:

  ```bash
  docker compose -f docker-compose.prod.yml down -v
  ```
* ❌ **Порт 8000 занят** →

  ```bash
  lsof -i :8000
  kill -9 <PID>
  ```

---

## 🛣️ Roadmap

* ✅ CRUD API
* ✅ Health-check
* ✅ Docker + Makefile
* ✅ Alembic + миграции
* ✅ Тесты (SQLite)
* ⏩ Сервисный слой (`services/`)
* ⏩ Планировщик обновлений базы
* ⏩ Telegram/CRM интеграция
* ⏩ Машинное обучение для прогноза решений

---

## 📚 Документация

* [DEPLOY.md](docs/DEPLOY.md) → деплой
* [LOCAL_DEV.md](docs/LOCAL_DEV.md) → локальная разработка
* [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) → частые ошибки
* [GIT_SETUP.md](docs/GIT_SETUP.md) → настройка Git

---

✅ Теперь у тебя полноценная документация, которая:

* описывает проект **от базы до API**,
* фиксирует **взаимодействие модулей**,
* даёт **практические инструкции** по запуску, миграциям и тестам,
* служит **паспортом проекта**.

---

Хочешь, я сразу сгенерирую для тебя и `docs/DEPLOY.md` + `docs/LOCAL_DEV.md`, чтобы документация была полностью завершена?
