# ⚖️ Legal Assistant Arbitrage API — v2

[![CI](https://github.com/your-org/legal-assistant-arbitrage-v2/actions/workflows/ci.yml/badge.svg)](https://github.com/your-org/legal-assistant-arbitrage-v2/actions/workflows/ci.yml)
[![Docs](https://github.com/your-org/legal-assistant-arbitrage-v2/actions/workflows/docs.yml/badge.svg)](docs/API_DOCS.md)

---

## 🔎 Логика сверху вниз (модули и фичи)

### 1. **Пользователи (`users`)**
- **Функции**:
  - регистрация, обновление, просмотр профиля;
  - роли (`admin`, `lawyer`, `client`).
- **Взаимосвязь**:
  - используют JWT (`auth`);
  - могут быть связаны с решениями (`decisions`).

### 2. **Авторизация (`auth`)**
- **Функции**:
  - регистрация пользователя (`/auth/register`);
  - вход (`/auth/login`);
  - получение текущего профиля (`/auth/me`);
  - выдача JWT-токена.
- **Взаимосвязь**:
  - базируется на `users`;
  - защищает роуты (`laws`, `decisions`).

### 3. **Законы (`laws`)**
- **Функции**:
  - CRUD по статьям кодексов;
  - хранение текста и метаданных норм права.
- **Взаимосвязь**:
  - связаны с решениями (`decisions`);
  - могут быть использованы для правового анализа.

### 4. **Судебные решения (`decisions`)**
- **Функции**:
  - CRUD судебных актов;
  - хранение номера дела, суда, даты, краткого описания.
- **Взаимосвязь**:
  - ссылаются на законы (`laws`);
  - могут быть связаны с пользователями (автор анализа).

### 5. **Health-check (`health`)**
- **Функции**:
  - проверка статуса API;
  - проверка соединения с БД.
- **Взаимосвязь**:
  - используется CI/CD и smoke-тестами.

### 6. **Сервисный слой (`services/`)**
- **Функции**:
  - инкапсулирует бизнес-логику (отдельно от роутов).
- **Взаимосвязь**:
  - роуты → вызывают сервисы → сервисы → работают с БД.

---

## 🔗 Диаграмма зависимостей модулей

```mermaid
flowchart TD

    subgraph API
        A1[Auth Routes] -->|JWT| A2[Users Routes]
        A2 --> A3[Laws Routes]
        A3 --> A4[Decisions Routes]
        A5[Health Route]
    end

    subgraph Services
        S1[Auth Service] --> U[Users Service]
        U --> L[Laws Service]
        L --> D[Decisions Service]
    end

    subgraph Schemas
        SchU[User Schemas]
        SchL[Law Schemas]
        SchD[Decision Schemas]
        SchT[Token Schema]
    end

    subgraph ORM
        M1[User Model]
        M2[Law Model]
        M3[Decision Model]
    end

    subgraph DB
        DB[(PostgreSQL / SQLite)]
    end

    %% Connections
    API --> Services
    Services --> Schemas
    Services --> ORM
    ORM --> DB
    A5 --> DB
________________________________________
🚀 Onboarding Checklist
1.	Клонируй репозиторий
2.	git clone https://github.com/your-org/legal-assistant-arbitrage-v2.git
3.	cd legal-assistant-arbitrage-v2
4.	Создай окружение
5.	python3.12 -m venv venv
6.	source venv/bin/activate
7.	pip install -r requirements-dev.txt
8.	Скопируй .env.example → .env и заполни.
9.	Запусти контейнеры
10.	make up
11.	Проверь API
12.	make health-host
13.	Примени миграции
14.	make migrate
15.	Запусти тесты
16.	make test
17.	Сгенерируй API Docs
18.	make apidocs
19.	Открой Swagger → http://127.0.0.1:8080/docs
________________________________________
📌 Цели проекта
•	База норм права и судебной практики.
•	Автоматический правовой анализ.
•	Шансы на успех по аналогичной практике.
•	Генерация процессуальных документов.
•	Финансовый калькулятор (госпошлина).
________________________________________
🧭 Архитектура (снизу вверх)
•	DB → PostgreSQL (prod/dev), SQLite (тесты).
•	ORM → SQLAlchemy ORM + Alembic миграции.
•	Schemas → Pydantic v2 (валидация API).
•	Services → бизнес-логика.
•	API → FastAPI (роуты /api/*).
•	CI/CD → GitHub Actions + smoke-тесты.
________________________________________
📂 Структура проекта
legal-assistant-arbitrage-v2/
├── backend/
│   ├── app/
│   │   ├── routes/     # API роуты (auth, users, laws, decisions, health)
│   │   ├── schemas/    # Pydantic схемы
│   │   ├── services/   # бизнес-логика
│   │   ├── models.py   # ORM-модели
│   │   ├── database.py # движок БД
│   │   └── main.py     # FastAPI точка входа
│   ├── alembic/        # миграции
│   └── seeds/          # сиды
├── docs/               # документация
├── docker-compose*.yml # окружение
├── Makefile            # автоматизация
├── scripts/            # утилиты и smoke-тесты
└── requirements*.txt   # зависимости
________________________________________
⚙️ Конфигурация
Файл .env:
POSTGRES_USER=admin
POSTGRES_PASSWORD=Admin@2025!
POSTGRES_DB=legal_assistant_db
POSTGRES_HOST=db
POSTGRES_PORT=5432
USE_SQLITE=0
SECRET_KEY=super_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
________________________________________
▶️ Запуск
Локально
make run
В Docker (prod)
make rebuild
make health-host
________________________________________
🗄️ Миграции
make makemigrations
make migrate
________________________________________
🧪 Тесты
make test
make smoke
________________________________________
🛠️ Makefile
Все команды:
make help
________________________________________
🤖 CI/CD
•	ci.yml → линтеры, миграции, pytest.
•	docs.yml → автогенерация API Docs.
________________________________________
📖 API Docs
Генерация:
make apidocs
Файл: docs/API_DOCS.md
________________________________________
🛣️ Roadmap
•	✅ CRUD API (users, laws, decisions)
•	✅ JWT авторизация
•	✅ Docker + Makefile
•	✅ Alembic миграции
•	✅ CI/CD + автодоки
•	⏩ Services слой (services/)
•	⏩ Планировщик обновлений БД
•	⏩ Интеграция Telegram/CRM
•	⏩ ML-модуль для прогноза решений
________________________________________

---

🔥 Теперь README полностью дополнен и содержит **Mermaid-диаграмму зависимостей**.

Хочешь, я ещё соберу такой же **диаграммой последовательности (sequence diagram)** сценарий "Регистрация → Авторизация → Создание закона → Создание решения"? Это будет визуальный флоу для юзкейсов.

