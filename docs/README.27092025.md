Отлично 👍
Держи полный, переписанный **README.v2.md** — с новыми разделами **"Git setup"** и **"Как подключить GitHub-репозиторий"**, полностью, без сокращений и изъятий.

---

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

* **Надёжность и воспроизводимость**: контейнеризация + CI + миграции + фиксация зависимостей.
* **Безопасность по умолчанию**: секреты в переменных окружения/секрет-хранилище, минимальные права БД.
* **Чистые интерфейсы**: строгие Pydantic-схемы (v2, `from_attributes=True`), понятные коды ошибок.
* **Изоляция слоёв**: веб-роуты / сервисы / модели / схемы разнесены.
* **SQLite для тестов**, PostgreSQL — в dev/prod.
* **Автогенерация документации** из OpenAPI + автосбор в CI.
* **Makefile** — удобные команды для разработчиков.

---

## 📁 Структура проекта

```
legal-assistant-arbitrage-v2/
├── .env.example
├── .gitignore
├── Dockerfile
├── Makefile
├── backend/
│   ├── alembic/
│   └── app/
│       ├── database.py
│       ├── main.py
│       ├── models.py
│       ├── routes/
│       ├── schemas/
│       ├── services/
│       └── tests/
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
```

---

## ⚙️ Подготовка окружения

### Установка инструментов

```bash
sudo apt update
sudo apt install -y python3.12-venv python3-pip git make
```

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
POSTGRES_USER=admin
POSTGRES_PASSWORD=Admin@2025!
POSTGRES_DB=legal_assistant_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

SECRET_KEY=super_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

TEST_SQLITE=0
OPENAPI_JSON_PATH=docs/openapi.json
```

---

## 🗄️ База данных и миграции

Инициализация:

```bash
alembic upgrade head
```

---

## ▶️ Запуск API (локально)

```bash
make run
```

Доступ:

* Swagger UI → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* Healthcheck → [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

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

---

## 🧪 Тестирование

Запуск тестов (SQLite):

```bash
make test
```

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
* Для продакшена: Sentry (ошибки), Prometheus (метрики).

---

## 🔐 Роли пользователей

* **admin** → полный доступ, управление пользователями и базой.
* **lawyer** → работа с запросами, анализ, добавление практики.
* **client** → подача запросов, просмотр результатов.

---

## 🔨 Makefile (удобные команды)

```makefile
run:        запуск локального API
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
* Убедись, что `POSTGRES_DB=legal_assistant_db` (а не `admin`)
* Удали volume и пересоздай:

```bash
docker compose -f docker-compose.prod.yml down -v
docker compose -f docker-compose.prod.yml up --build -d
```

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

---

## 🔗 Как подключить GitHub-репозиторий

1. Создай новый репозиторий на GitHub: [https://github.com/new](https://github.com/new)
   Название: `legal-assistant-arbitrage-v2`

2. Привяжи удалённый:

```bash
git remote add origin git@github.com:aw56/legal-assistant-arbitrage-v2.git
```

3. Первый пуш:

```bash
git branch -M main
git push -u origin main
```

---

✅ Теперь проект готов для работы всей командой: локально, через Docker и в CI/CD.

---

Хочешь, я сразу подготовлю отдельный `docs/GIT_SETUP.md`, чтобы это было вынесено из README и удобно ссылалось изнутри?
