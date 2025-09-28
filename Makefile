# ============================================
# 📘 Legal Assistant Arbitrage v2 — Makefile
# ============================================

# Python virtualenv
VENV = . venv/bin/activate &&

# ============================================
# 🔹 Основные команды разработки
# ============================================

# Запуск API (локально, в foreground)
run:
	$(VENV) uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload

# Запуск API в фоне
run-bg:
	$(VENV) nohup uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload > server.log 2>&1 &
	@echo "🚀 Сервер запущен в фоне. Логи: tail -f server.log"

# Остановка фонового сервера
stop-bg:
	pkill -f "uvicorn backend.app.main:app" || true
	@echo "🛑 Сервер остановлен"

# Просмотр логов
logs:
	tail -f server.log

# ============================================
# 🔹 База данных и миграции
# ============================================

# Запуск alembic миграций
alembic:
	$(VENV) alembic upgrade head

# Очистка локальной SQLite
clean-db:
	rm -f test.db
	@echo "🗑️ test.db удалён"

# ============================================
# 🔹 Тестирование
# ============================================

# Запуск pytest с SQLite
test:
	$(VENV) TEST_SQLITE=1 pytest -v

# Полная проверка: форматирование + тесты + линтеры
check: format lint test

# ============================================
# 🔹 Документация
# ============================================

# Генерация OpenAPI JSON
docs:
	$(VENV) python scripts/generate_openapi_json.py

# ============================================
# 🔹 Docker
# ============================================

# Запуск в dev-режиме
docker:
	docker compose up --build

# Запуск в прод-режиме
docker-prod:
	docker compose -f docker-compose.prod.yml up -d --build

# Полная очистка контейнеров и volume
docker-reset:
	docker compose -f docker-compose.prod.yml down -v
	@echo "🔄 Docker volume и контейнеры удалены"

# ============================================
# 🔹 Переключение окружений
# ============================================

# Локальная разработка (SQLite)
env-local:
	cp .env.example .env && echo "USE_SQLITE=1" >> .env
	@echo "✅ Переключено на локальное окружение (SQLite)"

# Продакшен (PostgreSQL)
env-prod:
	cp .env.example .env && sed -i '/USE_SQLITE/d' .env
	@echo "✅ Переключено на прод окружение (PostgreSQL)"

# ============================================
# 🔹 Кодстайл и линтеры
# ============================================

# Установка dev-зависимостей
dev-install:
	$(VENV) pip install black isort flake8 pre-commit

# Форматирование кода
format:
	$(VENV) black backend scripts
	$(VENV) isort backend scripts

# Проверка стиля
lint:
	$(VENV) black --check backend scripts
	$(VENV) isort --check-only backend scripts
	$(VENV) flake8 backend scripts

# ============================================
# 🔹 Pre-commit hooks
# ============================================

# Установка pre-commit в проект
pre-commit-install:
	$(VENV) pre-commit install
	@echo "✅ pre-commit хуки установлены"

# Ручной запуск pre-commit для всех файлов
pre-commit-run:
	$(VENV) pre-commit run --all-files

# ============================================
# 🔹 Утилиты
# ============================================

# Очистка pycache
clean-pycache:
	find . -type d -name "__pycache__" -exec rm -rf {} +

# Полная очистка окружения (кэш + SQLite)
reset: clean-pycache clean-db
	@echo "🔄 Очистка завершена"

cleanup:
	. venv/bin/activate && bash scripts/cleanup_imports.sh

# Фиксировать и пушить изменения в GitHub.
save:
	@git add .
	@git commit -m "chore: save current state"
	@git push -u origin main
	@echo "✅ Изменения сохранены и отправлены в GitHub"
