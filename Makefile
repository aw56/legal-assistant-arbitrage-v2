# ================================
# 📦 Legal Assistant Arbitrage v2
# Makefile для управления проектом
# ================================

# --- Default goal ---
.DEFAULT_GOAL := help

# --- Docker ---
up: ## 🚀 Запуск контейнеров (prod)
	docker compose -f docker-compose.prod.yml up -d --build

down: ## ⏹️ Остановка контейнеров
	docker compose -f docker-compose.prod.yml down

rebuild: ## 🔄 Полный пересоздание контейнеров с volume
	docker compose -f docker-compose.prod.yml down --volumes --remove-orphans
	docker compose -f docker-compose.prod.yml up -d --build --force-recreate

logs: ## 📜 Просмотр логов контейнеров
	docker compose -f docker-compose.prod.yml logs -f

ps: ## 📋 Список контейнеров
	docker compose -f docker-compose.prod.yml ps

shell: ## 🐚 Зайти внутрь контейнера backend
	docker compose -f docker-compose.prod.yml exec backend bash

# --- Alembic / DB ---
migrate: ## 🗄️ Применить миграции
	docker compose -f docker-compose.prod.yml exec backend alembic upgrade head

makemigrations: ## ✍️ Создать новую миграцию
	docker compose -f docker-compose.prod.yml exec backend alembic revision --autogenerate -m "new migration"

# --- Healthcheck ---
health-host: ## ❤️ Проверка API с хоста
	curl -s http://127.0.0.1:8080/api/health | jq

health-container: ## ❤️ Проверка API из контейнера
	docker compose -f docker-compose.prod.yml exec backend curl -s http://127.0.0.1:8000/api/health | jq

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

# --- Help ---
help: ## 📖 Показать список доступных команд
	@echo "=== 🛠 Доступные команды Makefile ==="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'
