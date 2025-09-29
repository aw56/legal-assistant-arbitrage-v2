# ============================================
# 📘 Legal Assistant Arbitrage v2 — Makefile
# ============================================

# Python virtualenv
VENV = . venv/bin/activate &&

# Docker image
DOCKER_USERNAME ?= alwalz
DOCKER_IMAGE = $(DOCKER_USERNAME)/legal-assistant-arbitrage-v2

# ============================================
# 🔹 Help
# ============================================

.PHONY: help
help: ## Показать список доступных команд
	@echo ""
	@echo "📘 Legal Assistant Arbitrage v2 — Makefile"
	@echo "============================================"
	@grep -E '^[a-zA-Z0-9_-]+:.*?##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf " \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""

# ============================================
# 🔹 Основные команды разработки
# ============================================

.PHONY: run run-bg stop-bg logs
run: ## Запуск API (локально, в foreground)
	$(VENV) uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload

run-bg: ## Запуск API в фоне
	$(VENV) nohup uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload > server.log 2>&1 &
	@echo "🚀 Сервер запущен в фоне. Логи: tail -f server.log"

stop-bg: ## Остановка фонового сервера
	pkill -f "uvicorn backend.app.main:app" || true
	@echo "🛑 Сервер остановлен"

logs: ## Просмотр логов
	tail -f server.log

# ============================================
# 🔹 База данных и миграции
# ============================================

.PHONY: alembic clean-db
alembic: ## Применить alembic миграции
	$(VENV) alembic upgrade head

clean-db: ## Очистить локальную SQLite
	rm -f test.db
	@echo "🗑️ test.db удалён"

# ============================================
# 🔹 Тестирование
# ============================================

.PHONY: test check
test: ## Запуск pytest с SQLite
	$(VENV) TEST_SQLITE=1 pytest -v

check: format lint test ## Полная проверка: форматирование + тесты + линтеры

# ============================================
# 🔹 Документация
# ============================================

.PHONY: docs
docs: ## Сгенерировать OpenAPI документацию
	PYTHONPATH=. $(VENV) python scripts/generate_openapi_docs.py

# ============================================
# 🔹 Docker
# ============================================

.PHONY: docker docker-prod docker-reset docker-build docker-push docker-run docker-login
docker: ## Запуск в dev-режиме
	docker compose up --build

docker-prod: ## Запуск в прод-режиме
	docker compose -f docker-compose.prod.yml up -d --build

docker-reset: ## Очистить контейнеры и volume
	docker compose -f docker-compose.prod.yml down -v
	@echo "🔄 Docker volume и контейнеры удалены"

docker-build: ## Собрать Docker-образ
	docker build -t $(DOCKER_IMAGE):latest .

docker-login: ## Логин в Docker Hub (использует DOCKER_USERNAME и DOCKER_PASSWORD)
	@if [ -z "$(DOCKER_PASSWORD)" ]; then \
		echo "❌ Укажи DOCKER_PASSWORD (например, export DOCKER_PASSWORD=xxx)"; \
		exit 1; \
	fi
	echo "$(DOCKER_PASSWORD)" | docker login -u "$(DOCKER_USERNAME)" --password-stdin

docker-push: docker-build ## Запушить Docker-образ в Docker Hub
	$(MAKE) docker-login
	docker push $(DOCKER_IMAGE):latest

docker-run: ## Запустить Docker-образ (убивает процессы на 8000)
	@if lsof -i :8000 | grep LISTEN; then \
		echo "⚠️ Порт 8000 занят — освобождаем..."; \
		pkill -f "uvicorn backend.app.main:app" || true; \
		docker ps -q --filter publish=8000 | xargs -r docker stop; \
	fi
	docker run -d -p 8000:8000 $(DOCKER_IMAGE):latest
	@echo "🚀 Контейнер запущен: http://127.0.0.1:8000"

# ============================================
# 🔹 Переключение окружений
# ============================================

.PHONY: env-local env-prod
env-local: ## Переключение на локальное окружение (SQLite)
	cp .env.example .env && echo "USE_SQLITE=1" >> .env
	@echo "✅ Переключено на локальное окружение (SQLite)"

env-prod: ## Переключение на прод окружение (PostgreSQL)
	cp .env.example .env && sed -i '/USE_SQLITE/d' .env
	@echo "✅ Переключено на прод окружение (PostgreSQL)"

# ============================================
# 🔹 Кодстайл и линтеры
# ============================================

.PHONY: dev-install format lint
dev-install: ## Установить dev-зависимости
	$(VENV) pip install black isort flake8 pre-commit

format: ## Форматировать код
	$(VENV) black backend scripts
	$(VENV) isort backend scripts

lint: ## Проверить стиль
	$(VENV) black --check backend scripts
	$(VENV) isort --check-only backend scripts
	$(VENV) flake8 backend scripts

# ============================================
# 🔹 Pre-commit hooks
# ============================================

.PHONY: pre-commit-install pre-commit-run
pre-commit-install: ## Установить pre-commit хуки
	$(VENV) pre-commit install
	@echo "✅ pre-commit хуки установлены"

pre-commit-run: ## Запустить pre-commit для всех файлов
	$(VENV) pre-commit run --all-files

# ============================================
# 🔹 Утилиты
# ============================================

.PHONY: clean-pycache reset cleanup save
clean-pycache: ## Очистить pycache
	find . -type d -name "__pycache__" -exec rm -rf {} +

reset: clean-pycache clean-db ## Полная очистка окружения
	@echo "🔄 Очистка завершена"

cleanup: ## Очистка импортов и неиспользуемого кода
	. venv/bin/activate && bash scripts/cleanup_imports.sh

save: ## Зафиксировать и пушить изменения в GitHub
	@git add .
	@git commit -m "chore: save current state"
	@git push -u origin main
	@echo "✅ Изменения сохранены и отправлены в GitHub"
