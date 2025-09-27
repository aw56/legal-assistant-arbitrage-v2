Принято ✅
Я полностью перепишу `README.v2.md` без изъятий и сокращений. Включу в него всё: цели, архитектуру, структуру, работу с окружением, локальную разработку, Docker, роли, эндпоинты, мониторинг, troubleshooting, дорожную карту **и полный Makefile прямо внутри документа**.

---

# 📘 Legal Assistant API — v2

Проект: **цифровой помощник юриста по арбитражным делам**
Стек: **Python 3.12 · FastAPI · SQLAlchemy 2 · Pydantic v2 · Alembic · PostgreSQL (prod) · SQLite (tests)**

---

## 🔭 Цели проекта

1. Материальная и процессуальная база по арбитражным спорам (нормы + практика).
2. Регулярная актуализация базы.
3. Стандартизированная форма клиентского запроса.
4. Правовой анализ (иерархия норм и практики).
5. Подсветка коллизий и рекомендации по их разрешению.
6. Мотивированное решение (каждый вывод обоснован).
7. Оценка шансов в % на основе практики.
8. Субъективные предпосылки для обращения в суд.
9. Типовые документы (списки и формы).
10. Автономность и локализация помощника.
11. Калькулятор стоимости (с коэффициентами).
12. Маркетинг и продвижение практики.

---

## 🧭 Архитектурные принципы

* Контейнеризация, CI, миграции.
* Секреты только в env.
* Строгие Pydantic v2 схемы.
* Изоляция слоёв (routes, services, schemas, models).
* SQLite для тестов, PostgreSQL для dev/prod.
* Автогенерация документации.
* Makefile: удобные команды.

---

## 📂 Структура проекта

```
legal-assistant-arbitrage-v2/
├─ .env                # текущее окружение
├─ .env.local          # окружение для локальной разработки
├─ .env.prod           # окружение для продакшена (Docker)
├─ .env.example        # шаблон
├─ Makefile
├─ Dockerfile
├─ docker-compose.yml
├─ docker-compose.prod.yml
├─ requirements.txt
├─ wait-for-db.sh
├─ backend/
│  ├─ alembic.ini
│  ├─ alembic/
│  │  ├─ env.py
│  │  └─ versions/
│  └─ app/
│     ├─ main.py
│     ├─ database.py
│     ├─ models.py
│     ├─ schemas/
│     ├─ routes/
│     ├─ services/
│     ├─ utils/
│     └─ tests/
└─ docs/
   ├─ API_DOCS.md
   ├─ PROJECT_DOC.md
   ├─ DEPLOY.md
   ├─ LOCAL_DEV.md
   └─ TROUBLESHOOTING.md
```

---

## ⚙️ Работа с окружением

### 🔹 Python venv

Создание окружения:

```bash
make venv
```

Активация:

```bash
source venv/bin/activate
```

Выход:

```bash
deactivate
```

Если папки `venv/` нет:

```bash
python3 -m venv venv
```

### 🔹 Переключение `.env`

* Локальное окружение:

  ```bash
  make env-local
  ```
* Продакшен окружение:

  ```bash
  make env-prod
  ```

---

## 🛠 Локальная разработка

Установка зависимостей:

```bash
make deps
```

Запуск API:

```bash
make run
```

Запуск в фоне:

```bash
make run-bg
```

Остановка:

```bash
make stop
```

Тесты:

```bash
make test
```

Документация API:

```bash
make docs
```

---

## 🐳 Продакшен (Docker)

Запуск:

```bash
make env-prod
make docker-prod
```

Остановка:

```bash
make docker-prod-down
```

Перезапуск:

```bash
make docker-prod-restart
```

Логи:

```bash
make logs service=backend
make logs service=db
```

---

## 🔐 Роли пользователей

* **admin**: управление пользователями, законами, решениями
* **lawyer**: доступ к базе, анализ, документы
* **client**: создание запросов и получение анализа

---

## 📜 Основные эндпоинты

* `GET /health` — healthcheck
* `/api/users/` — CRUD пользователей
* `/api/laws/` — CRUD законов
* `/api/decisions/` — CRUD судебных решений
* `/api/requests/` — клиентские запросы
* `/analyze/` — анализ запроса
* `/pricing/quote` — калькулятор стоимости

---

## 🧩 Makefile (полный)

```makefile
.PHONY: venv deps run run-bg stop test alembic-up docs \
        docker-prod docker-prod-down docker-prod-restart \
        env-local env-prod \
        kill-8000 kill-port logs

# ──────────────── БАЗОВЫЕ КОМАНДЫ ────────────────

venv:
	python3 -m venv venv

deps:
	. venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt && npm install -g openapi-markdown-cli

run:
	. venv/bin/activate && uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload

run-bg:
	nohup . venv/bin/activate && uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload > server.log 2>&1 &
	@echo "✅ Backend запущен в фоне (лог в server.log)"

stop:
	@PID=$$(pgrep -f "uvicorn backend.app.main:app" || true); \
	if [ -n "$$PID" ]; then \
		echo "🛑 Останавливаю процессы: $$PID"; \
		kill -9 $$PID; \
	else \
		echo "✅ Нет активных uvicorn процессов"; \
	fi

test:
	. venv/bin/activate && TEST_SQLITE=1 pytest -v

alembic-up:
	. venv/bin/activate && alembic upgrade head

docs:
	. venv/bin/activate && python scripts/generate_openapi_json.py && npx openapi-markdown-cli -i docs/openapi.json -o docs/API_DOCS.md

# ──────────────── DOCKER ────────────────

docker-prod:
	docker compose -f docker-compose.prod.yml up --build -d

docker-prod-down:
	docker compose -f docker-compose.prod.yml down

docker-prod-restart:
	docker compose -f docker-compose.prod.yml down && docker compose -f docker-compose.prod.yml up --build -d

# ──────────────── ОКРУЖЕНИЯ ────────────────

env-local:
	cp .env.local .env
	@echo "✅ Локальное окружение (.env.local → .env) активировано."

env-prod:
	cp .env.prod .env
	@echo "✅ Продакшен окружение (.env.prod → .env) активировано."

# ──────────────── УТИЛИТЫ ────────────────

kill-8000:
	@PID=$$(sudo lsof -t -i:8000 2>/dev/null); \
	if [ -n "$$PID" ]; then \
		echo "🛑 Убиваем процесс(ы) на порту 8000: $$PID"; \
		sudo kill -9 $$PID; \
	else \
		echo "✅ Порт 8000 свободен"; \
	fi

kill-port:
	@if [ -z "$(PORT)" ]; then \
		echo "⚠️  Использование: make kill-port PORT=XXXX"; \
	else \
		PID=$$(sudo lsof -t -i:$(PORT) 2>/dev/null); \
		if [ -n "$$PID" ]; then \
			echo "🛑 Убиваем процесс(ы) на порту $(PORT): $$PID"; \
			sudo kill -9 $$PID; \
		else \
			echo "✅ Порт $(PORT) свободен"; \
		fi; \
	fi

logs:
	@if [ -z "$(service)" ]; then \
		echo "⚠️  Использование: make logs service=backend|db"; \
	else \
		docker logs -f legal-assistant-arbitrage-v2-$(service)-1; \
	fi
```

---

## 🧩 Логи и мониторинг

* Логи backend:

  ```bash
  make logs service=backend
  ```
* Логи базы:

  ```bash
  make logs service=db
  ```
* Ошибки → [Sentry](https://sentry.io/)
* Метрики → Prometheus + Grafana

---

## 🧨 Troubleshooting

Типовые проблемы и решения вынесены в отдельный файл 👉 [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

---

## 🛣️ Дорожная карта

**Сделано:**

* ✅ Новая структура проекта (v2)
* ✅ CI + автогенерация документации
* ✅ Docker Compose (dev/prod)
* ✅ Скрипт ожидания БД
* ✅ Makefile с расширенными командами
* ✅ Healthcheck эндпоинт
* ✅ Роли пользователей
* ✅ Локальный run-bg и stop

**В планах:**

* ⏩ Импорт нормативной базы и судебной практики
* ⏩ Автоматическая актуализация базы
* ⏩ Расширенный калькулятор стоимости
* ⏩ Интеграция с Telegram/CRM
* ⏩ Мониторинг (Prometheus + Grafana)
* ⏩ Ошибки в Sentry

---

## ✅ Итог

* Проект готов к запуску локально и в продакшене.
* Управление через Makefile (одной строкой).
* Есть поддержка фонового запуска (`make run-bg` / `make stop`).
* Документация разделена на части:

  * `PROJECT_DOC.md` — архитектура
  * `DEPLOY.md` — деплой
  * `LOCAL_DEV.md` — локальная разработка
  * `TROUBLESHOOTING.md` — отладка
* Дорожная карта обновлена.

---

Хочешь, я теперь сделаю тебе такой же **финальный вариант для `docs/TROUBLESHOOTING.md`**, где соберу всё, включая Docker-проблемы и ошибки с портами?
