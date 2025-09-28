# === Makefile ===

run:
	. venv/bin/activate && nohup uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload > server.log 2>&1 &
	@echo "🚀 Сервер запущен в фоне. Логи: tail -f server.log"

test:
	@rm -f test.db
	. venv/bin/activate && TEST_SQLITE=1 pytest -v

alembic:
	. venv/bin/activate && alembic upgrade head

docs:
	. venv/bin/activate && python scripts/generate_openapi_json.py

docker:
	docker compose up --build

docker-prod:
	docker compose -f docker-compose.prod.yml up --build -d

env-local:
	cp .env.local .env

env-prod:
	cp .env.prod .env
