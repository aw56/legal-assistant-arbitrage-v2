# ================================
# 📦 Legal Assistant Arbitrage v2
# Makefile для управления проектом
# ================================

# --- Default goal ---
.DEFAULT_GOAL := help

# --- Переменные ---
COMPOSE_FILE = docker-compose.prod.yml
BACKEND_CONTAINER := $(shell docker compose -f $(COMPOSE_FILE) ps -q backend)

# ================================
# 📦 Зависимости
# ================================
install: ## 📦 Установить prod зависимости
	pip install -r requirements.txt

install-dev: ## 📦 Установить dev зависимости (prod + тесты/линтеры)
	pip install -r requirements-dev.txt

# --- Docker ---
up: ## 🚀 Запуск контейнеров (prod)
	docker compose -f $(COMPOSE_FILE) up -d --build

down: ## ⏹️ Остановка контейнеров
	docker compose -f $(COMPOSE_FILE) down

rebuild: ## 🔄 Полное пересоздание контейнеров с volume
	docker compose -f $(COMPOSE_FILE) down --volumes --remove-orphans
	docker compose -f $(COMPOSE_FILE) up -d --build --force-recreate

logs: ## 📜 Просмотр логов контейнеров
	docker compose -f $(COMPOSE_FILE) logs -f

ps: ## 📋 Список контейнеров
	docker compose -f $(COMPOSE_FILE) ps

shell: ## 🐚 Зайти внутрь контейнера backend
	docker exec -it $(BACKEND_CONTAINER) bash

# --- Alembic / DB ---
migrate: ## 🗄️ Применить миграции
	docker exec -it $(BACKEND_CONTAINER) alembic upgrade head

makemigrations: ## ✍️ Создать новую миграцию
	docker exec -it $(BACKEND_CONTAINER) alembic revision --autogenerate -m "new migration"

# --- Healthcheck ---
health-host: ## ❤️ Проверка API с хоста
	curl -s http://127.0.0.1:8080/api/health | jq

health-container: ## ❤️ Проверка API из контейнера
	docker exec -it $(BACKEND_CONTAINER) curl -s http://127.0.0.1:8000/api/health | jq

# --- Git ---
git-add: ## ➕ Добавить все изменения
	git add .

git-fix: ## 🧹 Запустить pre-commit hooks (black, isort, flake8 и т.д.)
	pre-commit run --all-files || true

git-commit: ## 💾 Сделать commit (пример: make git-commit m="fix: исправлена ошибка")
	@if [ -z "$(m)" ]; then \
		echo "❌ Укажи сообщение для коммита: make git-commit m=\"текст\""; \
		exit 1; \
	fi
	git commit -m "$(m)" --allow-empty || true

git-push: ## ⬆️ Отправить изменения в origin/main
	git push origin main

git-all: git-add git-fix ## 🚀 Полный цикл: add + commit + push (пример: make git-all m="feat: новая функция")
	@if [ -z "$(m)" ]; then \
		echo "❌ Укажи сообщение для коммита: make git-all m=\"текст\""; \
		exit 1; \
	fi
	git commit -m "$(m)" --allow-empty || true
	git push origin main

git-amend: ## ✏️ Изменить последний commit и переписать историю
	git add .
	pre-commit run --all-files || true
	git commit --amend --no-edit || true
	git push origin main --force

git-sync: ## 🔄 Подтянуть изменения из origin/main с сохранением локальных
	@git stash push -m "sync-stash" || true
	@git fetch origin main
	@git rebase origin/main || true
	@git stash pop || true

git-reset-hard: ## 💥 Сброс к origin/main (без сохранения изменений)
	@git fetch origin main
	@git reset --hard origin/main
	@echo "✅ Локальная ветка полностью сброшена и синхронизирована с origin/main"

git-reset-soft: ## 📝 Сброс к origin/main (с сохранением изменений в рабочей директории)
	@git fetch origin main
	@git reset --soft origin/main
	@echo "✅ Сброс к origin/main, изменения сохранены в рабочей директории"

git-fix: ## 🧹 Запустить pre-commit hooks (black, isort, flake8 и фиксы миграций)
	python3 scripts/fix_migrations.py || true
	pre-commit run --all-files || true
	@echo "✅ Авто-фиксы (pre-commit + миграции) применены"

# --- Tests ---
test: ## ✅ Запустить тесты
	docker exec -it $(BACKEND_CONTAINER) pytest backend/app/tests

test-verbose: ## 🐛 Запустить тесты с подробным выводом
	docker exec -it $(BACKEND_CONTAINER) pytest -vv backend/app/tests

docker-test: ## 🧪 Запустить все тесты внутри контейнера
	docker exec -it $(BACKEND_CONTAINER) pytest -vv

ci-test: ## 🤖 Запустить тесты в режиме CI/CD (без -it)
	docker exec $(BACKEND_CONTAINER) pytest -vv --maxfail=1 --disable-warnings -q

apidocs: ## 📖 Сгенерировать API_DOCS.md из OpenAPI
	python3 scripts/generate_docs.py

# ================================
# 🚀 Local FastAPI (uvicorn, venv)
# ================================
run: ## 🚀 Запуск локального FastAPI (uvicorn) в фоне
	nohup uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000 > uvicorn.log 2>&1 &
	@echo "✅ FastAPI (локально) запущен"

stop: ## ⏹️ Остановить локальный FastAPI
	@pkill -f "uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000" || true
	@echo "🛑 FastAPI (локально) остановлен"

status: ## 📋 Проверить, запущен ли локальный FastAPI
	@pgrep -a -f "uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000" || echo "❌ Локальный uvicorn не запущен"

logs: ## 📜 Логи локального FastAPI
	@tail -f uvicorn.log

restart: stop run ## 🔄 Перезапуск локального FastAPI

# ================================
# 🐳 Docker (prod/staging)
# ================================
ps-docker: ## 📋 Список контейнеров (docker-compose.prod.yml)
	docker compose -f docker-compose.prod.yml ps

logs-docker: ## 📜 Логи контейнеров (docker-compose.prod.yml)
	docker compose -f docker-compose.prod.yml logs -f

shell-docker: ## 🐚 Консоль внутри backend-контейнера
	docker compose -f docker-compose.prod.yml exec backend bash

lint: ## 🔎 Запустить pre-commit проверки локально
	pre-commit run --all-files

# --- Help ---
help: ## 📖 Показать список доступных команд
	@echo "=== 🛠 Доступные команды Makefile ==="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'
