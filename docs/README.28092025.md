Отлично, тогда держи полный переписанный **`README.md`** без сокращений, в духе предпоследней версии, но с учётом всех последних улучшений и нюансов:

```markdown
# 📘 Legal Assistant API — v2 (перезапуск с чистого листа)

Проект: **цифровой помощник юриста по арбитражным делам**
Стек: **Python 3.12 · FastAPI · SQLAlchemy 2 · Pydantic v2 · Alembic · PostgreSQL (prod) · SQLite (tests)**

---

## 🔭 Цели проекта

1. **Материальная и процессуальная база** по арбитражным спорам (нормы + практика).
2. **Регулярная актуализация** правовой базы.
3. **Стандартизированная форма клиентского запроса**.
4. **Правовой анализ** на основе базы (иерархия норм и практики).
5. Подсветка **коллизий** и рекомендации по их разрешению.
6. **Мотивированное решение** (каждый вывод обоснован нормами/практикой).
7. **Оценка шансов в %** с опорой на релевантную практику.
8. **Субъективные предпосылки** для обращения и представления в суде.
9. **Список и формы типовых документов**.
10. **Автономность и локализация** помощника.
11. **Калькулятор стоимости** (с понижающе-повышающими региональными коэффициентами).
12. **Маркетинговая стратегия** по продвижению практики арбитражных дел.

---

## 🧭 Архитектурные принципы v2

- **Надёжность и воспроизводимость**: контейнеризация + CI + миграции + фиксация зависимостей.
- **Безопасность по умолчанию**: секреты в переменных окружения/секрет-хранилище, минимальные права БД.
- **Чистые интерфейсы**: строгие Pydantic-схемы (v2, `from_attributes=True`), понятные коды ошибок.
- **Изоляция слоёв**: веб-роуты / сервисы / модели / схемы разнесены.
- **SQLite для тестов**, PostgreSQL — в dev/prod.
- **Автогенерация документации** из OpenAPI + автосбор в CI.
- **Makefile** — удобные команды для разработчиков.

---

## 📁 Структура проекта

```

legal-assistant-arbitrage-v2/
├── .env.example
├── .gitignore
├── Dockerfile
├── Makefile
├── backend/
│   ├── alembic/              # миграции
│   └── app/
│       ├── database.py
│       ├── main.py
│       ├── models.py
│       ├── routes/           # health, users, laws, decisions
│       ├── schemas/          # Pydantic-схемы
│       ├── services/         # бизнес-логика (на будущее)
│       └── tests/            # pytest
├── docker-compose.prod.yml
├── docker-compose.yml
├── docs/
│   ├── DEPLOY.md
│   ├── LOCAL_DEV.md
│   ├── README.v2.md
│   └── TROUBLESHOOTING.md
├── pytest.ini
├── requirements.txt
├── scripts/
│   └── generate_openapi_json.py
└── wait-for-db.sh

````

---

## ⚙️ Подготовка окружения

### Установка инструментов

```bash
sudo apt update
sudo apt install -y python3.12-venv python3-pip git make
````

(опционально: Docker и Compose)

```bash
sudo apt install -y docker.io docker-compose-plugin
sudo usermod -aG docker $USER
newgrp docker
```

---

## 📦 Установка зависимостей (локально)

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

## 🔐 Конфигурация окружения

`.env.example` копируется в `.env` и редактируется:

```dotenv
# === Локальная разработка с SQLite ===
USE_SQLITE=1

# PostgreSQL (docker/prod)
POSTGRES_USER=admin
POSTGRES_PASSWORD=Admin@2025!
POSTGRES_DB=legal_assistant_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# JWT и безопасность
SECRET_KEY=super_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# OpenAPI JSON
OPENAPI_JSON_PATH=docs/openapi.json

# Логирование
LOG_LEVEL=DEBUG
```

---

## 🗄️ База данных и миграции

### SQLite (тесты, локалка)

Создаётся автоматически: `test.db`.

### PostgreSQL (docker/prod)

Миграции через Alembic:

```bash
alembic upgrade head
```

---

## ▶️ Запуск API (локально)

```bash
make run
```

Запуск в фоне:

```bash
make run-bg
```

Доступ:

* Swagger UI → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* Healthcheck → [http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health)

---

## 🐳 Запуск через Docker Compose

### Dev

```bash
make docker
```

### Prod

```bash
make docker-prod
```

Остановка:

```bash
docker compose -f docker-compose.prod.yml down
```

---

## 🧪 Тестирование

Тесты используют SQLite (`test.db`).

### Запуск

```bash
make test
```

### Результат

* ✅ Все тесты должны проходить (`10 passed`).
* ⚠️ Возможны предупреждения от **SQLAlchemy** (`Query.get`) и **Pydantic** (`dict`/`Config`).

---

## 🤖 CI/CD

CI (GitHub Actions):

* линтеры
* pytest (SQLite)
* автогенерация OpenAPI → `docs/API_DOCS.md`

CD (черновик):

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

---

## 📊 Логи и мониторинг

* Логи пишутся в `server.log`.
* Для продакшена: **Sentry** (ошибки), **Prometheus** (метрики).

---

## 🔐 Роли пользователей

* **admin** → полный доступ, управление пользователями и базой.
* **lawyer** → работа с запросами, анализ, добавление практики.
* **client** → подача запросов, просмотр результатов.

---

## 🔨 Makefile (удобные команды)

```makefile
run:        запуск локального API
run-bg:     запуск API в фоне
test:       тесты (SQLite)
alembic:    миграции
docs:       генерация API-доки
docker:     запуск docker-compose.yml
docker-prod:запуск docker-compose.prod.yml
env-local:  переключение на .env.local
env-prod:   переключение на .env.prod
```

---

## 🧨 Troubleshooting

### Ошибка: порт 8000 занят

```bash
lsof -i :8000
kill -9 <PID>
```

### Контейнеры перезапускаются в цикле

* Проверь `.env`
* Убедись, что `POSTGRES_DB=legal_assistant_db`
* Удали volume и пересоздай:

```bash
docker compose -f docker-compose.prod.yml down -v
docker compose -f docker-compose.prod.yml up --build -d
```

### Ошибка: `psycopg2.OperationalError: connection refused`

* Используй SQLite (`USE_SQLITE=1`)
* Или проверь, что Postgres запущен.

---

## 🛣️ Дорожная карта

* ✅ CRUD (users, laws, decisions)
* ✅ Healthcheck
* ✅ Тесты (SQLite)
* ✅ Docker (dev + prod)
* ✅ CI (pytest + автодок)
* ⏩ Импорт нормативной базы
* ⏩ Планировщик обновлений
* ⏩ Интеграция с Telegram/CRM
* ⏩ Продвинутый анализ

---

## 🛠 Git setup

Один раз укажи имя и email (лучше использовать GitHub **noreply email**):

```bash
git config --global user.name "Aleksej Walz"
git config --global user.email "37653309+aw56@users.noreply.github.com"
```

Проверка:

```bash
git config --list | grep user
```

Инициализация проекта:

```bash
git init
git add .
git commit -m "feat: initial commit with CRUD routes, tests, and docker setup"
```

---

## 🔗 Как подключить GitHub-репозиторий

1. Сгенерируй SSH-ключ:

```bash
ssh-keygen -t ed25519 -C "alexejwalz@gmail.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

2. Скопируй публичный ключ:

```bash
cat ~/.ssh/id_ed25519.pub
```

3. Добавь его в GitHub → **Settings → SSH and GPG keys → New SSH key**.

4. Проверь подключение:

```bash
ssh -T git@github.com
# Hi aw56! You've successfully authenticated
```

5. Добавь remote:

```bash
git remote add origin git@github.com:aw56/legal-assistant-arbitrage-v2.git
git branch -M main
git push -u origin main
```

---

✅ Теперь проект готов к работе локально, через Docker и CI/CD.

```

---

Хочешь, я сразу вынесу разделы **Git setup** и **GitHub подключение** в отдельный `docs/GIT_SETUP.md`, а в README оставить только краткую ссылку?
```
