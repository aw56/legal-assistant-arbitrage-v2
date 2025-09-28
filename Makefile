# === Makefile для Legal Assistant Arbitrage ===

# Запуск локального сервера (в фоне)
run:
	. venv/bin/activate && nohup uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload > server.log 2>&1 &
	@echo "🚀 Сервер запущен в фоне. Логи: tail -f server.log"

# Запуск тестов (с SQLite)
test:
	. venv/bin/activate && TEST_SQLITE=1 pytest -v

# Локальное окружение
env-local:
	cp .env.local .env
	@echo "✅ Локальное окружение (.env.local → .env) активировано."
	$(MAKE) run

# Продакшн окружение (docker-compose)
env-prod:
	cp .env.prod .env
	@echo "✅ Продакшн окружение (.env.prod → .env) активировано."
	$(MAKE) docker-prod

# Docker запуск (прод)
docker-prod:
	docker compose -f docker-compose.prod.yml up --build -d

# Docker остановка
docker-down:
	docker compose -f docker-compose.prod.yml down

# Проверка логов сервера
logs:
	tail -f server.log

# Генерация OpenAPI JSON
openapi:
	. venv/bin/activate && python scripts/generate_openapi_json.py

# Удаление базы SQLite
reset-sqlite:
	rm -f test.db
	@echo "🗑️ SQLite база удалена."

# Полная пересборка docker
rebuild:
	docker compose -f docker-compose.prod.yml down -v --remove-orphans
	docker compose -f docker-compose.prod.yml up --build -d
