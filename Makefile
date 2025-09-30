# Makefile для управления docker-compose.prod.yml

up:
	docker compose -f docker-compose.prod.yml up -d --build

down:
	docker compose -f docker-compose.prod.yml down

rebuild:
	docker compose -f docker-compose.prod.yml down --volumes --remove-orphans
	docker compose -f docker-compose.prod.yml up -d --build --force-recreate

logs:
	docker compose -f docker-compose.prod.yml logs -f

ps:
	docker compose -f docker-compose.prod.yml ps

migrate:
	docker compose -f docker-compose.prod.yml exec backend alembic upgrade head

makemigrations:
	docker compose -f docker-compose.prod.yml exec backend alembic revision --autogenerate -m "new migration"

shell:
	docker compose -f docker-compose.prod.yml exec backend bash

health-host:
	curl -s http://127.0.0.1:8080/api/health | jq

health-container:
	docker compose -f docker-compose.prod.yml exec backend curl -s http://127.0.0.1:8000/api/health | jq
