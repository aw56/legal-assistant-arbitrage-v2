.PHONY: venv deps run test alembic-up docs \
        docker-prod docker-prod-down docker-prod-restart \
        env-local env-prod \
        kill-8000 kill-port

# ──────────────── БАЗОВЫЕ КОМАНДЫ ────────────────

# Создать виртуальное окружение
venv:
	python3 -m venv venv

# Установить зависимости (Python + OpenAPI CLI)
deps:
	. venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt && npm install -g openapi-markdown-cli

# Запуск локального сервера (FastAPI)
run:
	. venv/bin/activate && uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload

# Запуск тестов (SQLite)
test:
	. venv/bin/activate && TEST_SQLITE=1 pytest -v

# Применить миграции Alembic
alembic-up:
	. venv/bin/activate && alembic upgrade head

# Сгенерировать OpenAPI → Markdown
docs:
	. venv/bin/activate && python scripts/generate_openapi_json.py && npx openapi-markdown-cli -i docs/openapi.json -o docs/API_DOCS.md

# ──────────────── DOCKER ────────────────

# Запуск продакшена (Docker Compose)
docker-prod:
	docker compose -f docker-compose.prod.yml up --build -d

# Остановка продакшена
docker-prod-down:
	docker compose -f docker-compose.prod.yml down

# Перезапуск продакшена
docker-prod-restart:
	docker compose -f docker-compose.prod.yml down && docker compose -f docker-compose.prod.yml up --build -d

# ──────────────── ОКРУЖЕНИЯ ────────────────

# Переключение на локальное окружение
env-local:
	cp .env.local .env
	@echo "✅ Локальное окружение (.env.local → .env) активировано."

# Переключение на продакшен окружение
env-prod:
	cp .env.prod .env
	@echo "✅ Продакшен окружение (.env.prod → .env) активировано."

# ──────────────── УТИЛИТЫ ────────────────

# Убить процессы, держащие порт 8000
kill-8000:
	@PID=$$(sudo lsof -t -i:8000 2>/dev/null); \
	if [ -n "$$PID" ]; then \
		echo "🛑 Убиваем процесс(ы) на порту 8000: $$PID"; \
		sudo kill -9 $$PID; \
	else \
		echo "✅ Порт 8000 свободен"; \
	fi

# Убить процессы на любом порту: make kill-port PORT=XXXX
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
