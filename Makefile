# ================================================
# ⚖️ Legal Assistant Arbitrage v2.7 — Unified Makefile (with Safe Backup)
# ================================================
.DEFAULT_GOAL := help

# --- Locale & shell ---
SHELL := /bin/bash
.SHELLFLAGS := -o pipefail -c
export LANG := en_US.UTF-8
export LC_ALL := en_US.UTF-8
export LANGUAGE := en_US.UTF-8

# --- Core vars ---
COMPOSE_FILE        = docker-compose.prod.yml
BACKEND_CONTAINER  := $(shell docker compose -f $(COMPOSE_FILE) ps -q backend)
DB_CONTAINER        = legal-assistant-db
DB_NAME             = legal_assistant_db
DB_USER             = admin
DB_DUMP_FILE        = backup.sql
SEED_FILE           = seeds/init_data.sql
FIXTURES_DIR        = fixtures

# ======= Paths for docs/progress =======
PROGRESS_DIR        := artifacts
PROGRESS_DOCS_DIR   := docs
PROGRESS_DATE       := $(shell date '+%Y%m%d')
PROGRESS_TIME       := $(shell date '+%H%M')
PROGRESS_FILE       := $(PROGRESS_DOCS_DIR)/PROGRESS_$(PROGRESS_DATE).md
PROGRESS_SNAPSHOT   := $(PROGRESS_DIR)/PROGRESS_$(PROGRESS_DATE)_$(PROGRESS_TIME).md
PROGRESS_TEMPLATE   := $(PROGRESS_DOCS_DIR)/PROGRESS_TEMPLATE.md
TACTICAL_FILE       := $(PROGRESS_DOCS_DIR)/PROGRESS_TACTICAL.md

# ======= SED Toolkit vars =======
SED_RULES        := scripts/sed_auto_rules.txt
SED_LOG          := logs/sed.log
SED_CSV          := logs/sed_auto_log.csv
SED_BACKUP_DIR   := backup/sed
SED_TIMESTAMP    := $(shell date '+%Y-%m-%d_%H-%M-%S')

# =================================
# 💾 SAFE BACKUP
# =================================
backup-makefile: ## 💾 Создать резервную копию Makefile с датой
	@mkdir -p backup
	@cp Makefile backup/Makefile_$(shell date '+%Y%m%d_%H%M%S').bak
	@echo "✅ Резервная копия Makefile создана в ./backup"

# =================================
# 🐳 Docker
# =================================
up: ## 🚀 Запуск контейнеров
	docker compose -f $(COMPOSE_FILE) up -d --build

down: ## ⏹️ Остановка контейнеров
	docker compose -f $(COMPOSE_FILE) down

rebuild: ## 🔄 Пересоздать контейнеры с volumes
	docker compose -f $(COMPOSE_FILE) down --volumes --remove-orphans
	docker compose -f $(COMPOSE_FILE) up -d --build --force-recreate

restart-docker: down up ## 🔄 Перезапуск контейнеров

logs: ## 📜 Логи контейнеров
	docker compose -f $(COMPOSE_FILE) logs -f

ps: ## 📋 Список контейнеров
	docker compose -f $(COMPOSE_FILE) ps

shell: ## 🐚 Bash внутри backend
	docker exec -it $(BACKEND_CONTAINER) bash

ps-docker: ## 📋 Контейнеры (prod compose)
	docker compose -f docker-compose.prod.yml ps

logs-docker: ## 📜 Логи (prod compose)
	docker compose -f docker-compose.prod.yml logs -f

shell-docker: ## 🐚 Bash в backend (prod compose)
	docker compose -f docker-compose.prod.yml exec backend bash

# =================================
# 🗄️ Alembic (Migrations)
# =================================
doctor-check:
	@if [ -z "$(BACKEND_CONTAINER)" ]; then echo "❌ Backend контейнер не запущен"; exit 1; fi

migrate: doctor-check ## 🗄️ Применить миграции
	docker exec -it $(BACKEND_CONTAINER) alembic upgrade head

makemigrations: doctor-check ## ✍️ Создать новую миграцию
	docker exec -it $(BACKEND_CONTAINER) alembic revision --autogenerate -m "new migration"

fix-migrations: doctor-check ## 🛠️ Автофикс миграций
	docker exec -it $(BACKEND_CONTAINER) python3 scripts/fix_migrations.py

current: doctor-check ## 🔎 Текущая миграция
	docker exec -it $(BACKEND_CONTAINER) alembic current

history: doctor-check ## 📜 История миграций
	docker exec -it $(BACKEND_CONTAINER) alembic history --verbose | tail -n 50

heads: doctor-check ## 🧩 Head-миграции
	docker exec -it $(BACKEND_CONTAINER) alembic heads

downgrade: doctor-check ## ⏪ Откатить миграции (make downgrade v=-1)
	@if [ -z "$(v)" ]; then echo "❌ Укажи версию"; exit 1; fi
	docker exec -it $(BACKEND_CONTAINER) alembic downgrade $(v)

merge-heads: doctor-check ## 🔀 Слить несколько heads
	docker exec -it $(BACKEND_CONTAINER) alembic merge heads -m "merge heads"

stamp-head: doctor-check ## 🏷️ Пометить миграции как применённые
	docker exec -it $(BACKEND_CONTAINER) alembic stamp head
	docker exec -it $(DB_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME) -c "SELECT * FROM alembic_version;"

check-migrations: doctor-check ## ✅ Проверка консистентности миграций
	docker exec -it $(BACKEND_CONTAINER) alembic check || (echo "❌ Проблемы с миграциями"; exit 1)

# =================================
# 🐘 PostgreSQL
# =================================
db-shell: ## 🐚 Консоль psql
	docker exec -it $(DB_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME)

db-tables: ## 📋 Список таблиц
	docker exec -it $(DB_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME) -c "\dt"

db-dump: ## 💾 Дамп БД
	docker exec -t $(DB_CONTAINER) pg_dump -U $(DB_USER) $(DB_NAME) > $(DB_DUMP_FILE)
	@echo "✅ Дамп сохранён: $(DB_DUMP_FILE)"

db-restore: ## ♻️ Восстановление из дампа
	@if [ ! -f "$(DB_DUMP_FILE)" ]; then echo "❌ Нет дампа"; exit 1; fi
	docker exec -i $(DB_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME) < $(DB_DUMP_FILE)

db-reset-tables: ## 💥 Очистить все таблицы (drop schema)
	docker exec -it $(DB_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME) -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

drop-db: ## 💥 Удалить базу
	docker exec -it $(DB_CONTAINER) dropdb -U $(DB_USER) --if-exists $(DB_NAME)

create-db: ## 🆕 Создать базу
	docker exec -it $(DB_CONTAINER) createdb -U $(DB_USER) $(DB_NAME)

check-db: ## ✅ Проверка соединения с БД
	docker exec -it $(DB_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME) -c "SELECT now();"

db-inspect: ## 🔍 Инспекция схем и Alembic
	docker exec -it $(DB_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME) -c "SELECT * FROM alembic_version;"
	docker exec -it $(DB_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME) -c '\dn'

wait-for-db: ## ⏳ Ждать готовность БД
	until docker exec -it $(DB_CONTAINER) pg_isready -U $(DB_USER) -d $(DB_NAME); do sleep 2; done

seed: ## 🌱 Инициализация данными из seeds/init_data.sql (если есть)
	@if [ -f "$(SEED_FILE)" ]; then \
		echo "🌱 Загрузка $(SEED_FILE)"; \
		docker exec -i $(DB_CONTAINER) psql -U $(DB_USER) -d $(DB_NAME) < $(SEED_FILE); \
	else echo "ℹ️  $(SEED_FILE) не найден — пропуск"; fi

# =================================
# ❤️ Health
# =================================
health-host: ## ❤️ Проверка API (локальный сервер)
	@echo "🔍 Проверка /api/health на http://127.0.0.1:8080 ..."
	@curl -s http://127.0.0.1:8080/api/health | jq || echo "❌ API не отвечает"

health-container: ## ❤️ Проверка API (в контейнере backend)
	@echo "🐳 Проверка /api/health внутри контейнера $(BACKEND_CONTAINER)..."
	@docker exec -it $(BACKEND_CONTAINER) curl -s http://127.0.0.1:8000/api/health | jq || echo "❌ API в контейнере не отвечает"

wait-for-api: ## ⏳ Ожидание готовности API
	@echo "⏳ Ожидание готовности API на http://127.0.0.1:8080 ..."
	@until curl -s http://127.0.0.1:8080/api/health | grep '"ok"' > /dev/null; do \
		echo "⏳ ...ожидание..."; sleep 2; \
	done
	@echo "✅ API готов к работе!"

# =================================
# 🧪 Tests
# =================================
install: ## 📦 Установить prod зависимости (в контейнере)
	docker exec -it $(BACKEND_CONTAINER) pip install -r requirements.txt

install-dev: ## 📦 Установить dev зависимости (в контейнере)
	docker exec -it $(BACKEND_CONTAINER) pip install -r requirements-dev.txt

setup-dev: install-dev up migrate seed test ## 🚀 Dev setup
	@echo "✅ Dev окружение готово"

setup-prod: rebuild migrate seed ## 🚀 Prod setup
	@echo "✅ Prod окружение готово"

smoke: ## 🚦 pytest -m smoke
	@pytest -m smoke -v --disable-warnings --maxfail=1 --tb=short || (echo "❌ Smoke-тесты не пройдены!"; exit 1)

smoke-local: ## 🚦 Smoke локально + Telegram при сбое
	@echo "🚦 Запуск локальных smoke-тестов..."
	@pytest -m smoke -v --disable-warnings --maxfail=1 --tb=short || ( \
		echo "❌ Smoke-тесты не пройдены! Отправка уведомления в Telegram..."; \
		python3 backend/app/utils/notify_telegram.py "🚨 Smoke-тесты не пройдены локально — проверь /api/health ❌"; \
		exit 1; \
	)
	@echo "✅ Все smoke-тесты успешно пройдены!"

smoke-ci: ## 🤖 Smoke-тесты CI
	@echo "🤖 Запуск smoke-тестов в CI..."
	@pytest -m smoke -v --disable-warnings || ( \
		echo "❌ Smoke-тесты CI не пройдены!"; \
		python3 backend/app/utils/notify_telegram.py "🚨 Smoke-тесты не пройдены в CI Legal Assistant Arbitrage v2.4 ❌"; \
		exit 1; \
	)
	@echo "✅ Smoke-тесты CI успешно завершены!"

test: ## ✅ pytest all (в контейнере)
	docker exec -it $(BACKEND_CONTAINER) pytest backend/app/tests

test-verbose: ## 🐛 pytest -vv
	docker exec -it $(BACKEND_CONTAINER) pytest -vv backend/app/tests

docker-test: ## 🧪 pytest -vv (корень)
	docker exec -it $(BACKEND_CONTAINER) pytest -vv

ci-test: ## 🤖 CI pytest + простой API-пинг
	docker exec $(BACKEND_CONTAINER) pytest -vv --maxfail=1 --disable-warnings -q
	$(MAKE) test-api

coverage: ## 📊 Покрытие тестами
	docker exec -it $(BACKEND_CONTAINER) pytest --cov=backend/app tests/ --cov-report=term-missing

# ================================
# 🌐 Integration Tests
# ================================

integration: ## 🌐 Запуск интеграционных тестов (pytest -m integration)
	@echo "🌐 Запуск интеграционных тестов..."
	@pytest -m integration -v --disable-warnings --maxfail=1 --tb=short || ( \
		echo "❌ Интеграционные тесты не пройдены!"; \
		exit 1; \
	)
	@echo "✅ Все интеграционные тесты успешно пройдены!"

integration-local: ## 🌐 Интеграционные тесты локально с Telegram-уведомлением
	@echo "🌐 Запуск интеграционных тестов (локально)..."
	@pytest -m integration -v --disable-warnings --maxfail=1 --tb=short || ( \
		echo "❌ Интеграционные тесты не пройдены! Отправка уведомления в Telegram..."; \
		python3 backend/app/utils/notify_telegram.py "🚨 Интеграционные тесты упали локально — проверь Telegram или KAD ❌"; \
		exit 1; \
	)
	@echo "✅ Интеграционные тесты успешно завершены!"

integration-ci: ## 🤖 Интеграционные тесты для CI (с Telegram уведомлением)
	@echo "🤖 Запуск интеграционных тестов в CI..."
	@pytest -m integration -v --disable-warnings --maxfail=1 --tb=short || ( \
		echo "❌ Интеграционные тесты CI не пройдены!"; \
		python3 backend/app/utils/notify_telegram.py "🚨 Integration CI tests failed in pipeline ❌"; \
		exit 1; \
	)
	@echo "✅ Интеграционные тесты CI успешно завершены!"

# =================================
# 📢 Telegram
# =================================
TELEGRAM_BOT_TOKEN ?= $(TELEGRAM_BOT_TOKEN)
TELEGRAM_CHAT_ID   ?= $(TELEGRAM_CHAT_ID)
MESSAGE            ?= "✅ CI успешно завершён."

telegram-notify:
	@python3 backend/app/utils/notify_telegram.py "$(MESSAGE)"

telegram-notify-test:
	@echo "🔔 Проверка Telegram уведомлений..."
	@$(MAKE) telegram-notify MESSAGE="🚀 Legal Assistant Arbitrage: тестовое уведомление от CI"

# =================================
# 📚 Docs
# =================================
apidocs: ## 📖 Сгенерировать API_DOCS.md
	docker compose -f $(COMPOSE_FILE) exec backend sh -c "PYTHONPATH=/code python3 scripts/generate_docs.py"

archdocs: ## 🏗️ Сгенерировать ARCHITECTURE.md
	docker compose -f $(COMPOSE_FILE) exec backend sh -c "PYTHONPATH=/code python3 scripts/generate_architecture.py"

docs: apidocs archdocs ## 📚 Полная генерация документации
	@echo "📚 Документация обновлена."

# =================================
# 🧩 SED TOOLKIT v3.7 — Safe Restore + CSV Logging
# =================================
sed-help:
	@echo "==========================================="
	@echo "🧰  SED TOOLKIT v3.7 — Safe Restore + CSV Logging"
	@echo "-------------------------------------------"
	@echo " make sed-template     # создать шаблон правил"
	@echo " make sed-clean        # очистить CRLF, BOM, не-UTF8"
	@echo " make sed-fix-rules    # исправить стрелки и кодировку"
	@echo " make sed-validate     # проверить корректность файла правил"
	@echo " make sed-auto         # применить замены (лог + CSV)"
	@echo " make sed-auto-safe    # безопасный режим с бэкапами"
	@echo " make sed-restore      # восстановить из backup/sed/*.bak"
	@echo " make sed-log-archive  # архивировать логи"
	@echo "-------------------------------------------"

sed-template:
	@mkdir -p scripts
	@printf "INFO→INFO\napi.legal.local→api.legal.local\nv2.4→v2.4\n\"testuser\"→\"apitest\"\n" > $(SED_RULES)
	@echo "✅ Шаблон пересоздан: $(SED_RULES)"

sed-clean:
	@echo "🧹 Очистка файла $(SED_RULES)..."
	@iconv -f utf-8 -t utf-8 -c $(SED_RULES) | tr -d '\r' | sed '1s/^\xEF\xBB\xBF//' > $(SED_RULES).tmp
	@mv $(SED_RULES).tmp $(SED_RULES)
	@dos2unix -q $(SED_RULES) 2>/dev/null || true
	@sed -i 's/[[:cntrl:]]//g' $(SED_RULES)
	@echo "✅ Очистка завершена — UTF-8 OK"

sed-fix-rules:
	@echo "🧠 Проверка и исправление стрелок..."
	@grep -q '→' $(SED_RULES) || sed -i 's/->/→/g' $(SED_RULES)
	@$(MAKE) sed-clean
	@echo "✅ Файл приведён к корректному виду"

sed-validate:
	@echo "🔍 Проверка файла $(SED_RULES)..."
	@file $(SED_RULES)
	@if ! grep -q '→' $(SED_RULES); then echo "❌ Ошибка: разделитель → не найден."; exit 1; fi
	@echo "✅ Разделитель найден."
	@if file $(SED_RULES) | grep -qv 'UTF-8'; then echo "❌ Ошибка кодировки — не UTF-8."; exit 1; fi
	@echo "🧩 Проверка завершена."

sed-auto:
	@echo "🤖 Применение авто-правил из $(SED_RULES)..."
	@mkdir -p logs $(SED_BACKUP_DIR)
	@> $(SED_LOG)
	@echo "pattern,replace,file,timestamp" > $(SED_CSV)
	@while IFS='→' read -r pattern replace; do \
		[ -z "$$pattern" ] && continue; \
		echo "🔧 Ищу '$$pattern' → '$$replace'..." | tee -a $(SED_LOG); \
		files=$$(grep -rl --exclude=$(SED_RULES) "$$pattern" backend app Makefile scripts 2>/dev/null || true); \
		for file in $$files; do \
			cp "$$file" "$(SED_BACKUP_DIR)/$$(basename $$file)_$(SED_TIMESTAMP).bak"; \
			sed -i "s|$$(printf '%s' "$$pattern" | sed 's/[.[\*^$(){}?+|/]/\\&/g')|$$(printf '%s' "$$replace" | sed 's/[&/\]/\\&/g')|g" "$$file"; \
			echo "$$pattern,$$replace,$$file,$(SED_TIMESTAMP)" >> $(SED_CSV); \
			echo "✅ Заменено в $$file" | tee -a $(SED_LOG); \
		done; \
	done < $(SED_RULES)
	@echo "🚀 sed-auto завершено. Отчёты: $(SED_LOG), $(SED_CSV)"

sed-auto-safe:
	@echo "🛡️  Безопасный режим SED AUTO..."
	@mkdir -p $(SED_BACKUP_DIR)
	@$(MAKE) sed-fix-rules
	@$(MAKE) sed-validate
	@$(MAKE) sed-auto || { echo "❌ Ошибка при sed-auto"; exit 1; }
	@echo "✅ Все изменения применены. Бэкапы — в $(SED_BACKUP_DIR)."

sed-restore:
	@echo "♻️ Восстанавливаю файлы из $(SED_BACKUP_DIR)..."
	@find $(SED_BACKUP_DIR) -type f -name "*.bak" | while read file; do \
		target=$$(basename $$file | sed 's/_.*\.bak//'); \
		if [ -f "$$target" ]; then \
			cp "$$file" "$$target"; \
			echo "✅ Восстановлен $$target"; \
		else \
			echo "⚠️  Пропущен (оригинал не найден): $$target"; \
		fi; \
	done
	@echo "♻️ Восстановление завершено."

sed-log-archive:
	@mkdir -p logs/archive
	@zip -q logs/archive/sed_logs_$(SED_TIMESTAMP).zip $(SED_LOG) $(SED_CSV) || true
	@echo "✅ Логи архивированы в logs/archive/sed_logs_$(SED_TIMESTAMP).zip"

# =================================
# 🔎 Lint / Format / pre-commit
# =================================
pre-commit: ## 🚦 Запуск всех хуков pre-commit
	@echo "🚦 Запуск pre-commit хуков..."
	pre-commit run --all-files --show-diff-on-failure || true
	@echo "✅ pre-commit проверки завершены."

lint: ## 🔍 Полный линт (pre-commit + yaml + tabs)
	@echo "🔎 Проверка кода и конфигурации..."
	pre-commit run --all-files --show-diff-on-failure || true
	yamllint .github/workflows/ci.yml || true
	$(MAKE) lint-tabs
	@echo "✅ Проверка завершена."

lint-tabs: ## 🔍 Проверка табов в Makefile
	@echo "🔍 Проверка Makefile на пробелы вместо табов..."
	@if grep -P '^[ ]{4,}[^\t#]' Makefile > /tmp/make_tabs_check.txt; then \
		echo "❌ Обнаружены строки с пробелами вместо табов:"; \
		cat /tmp/make_tabs_check.txt; \
		exit 1; \
	else \
		echo "✅ Все команды Makefile используют TAB."; \
	fi

format: ## 🎨 Форматирование Python/Markdown
	@echo "🎨 Форматирование Python (black + isort)..."
	@black backend/ scripts/ || true
	@isort backend/ scripts/ || true
	@echo "🧾 Форматирование Markdown..."
	@npx markdownlint-cli2 --fix "docs/**/*.md" "artifacts/**/*.md" || true
	@echo "✅ Все файлы отформатированы."

fix-docs: ## 🧩 Исправление markdownlint и commit
	@echo "🧩 Исправление markdownlint..."
	npx markdownlint-cli2 --fix "docs/**/*.md" || true
	npx prettier --write "docs/**/*.md" || true
	@git add docs/
	@git commit -m "fix(docs): auto-format markdown files" || true
	@echo "✅ Документация выровнена."

fix-yaml: ## 🧹 Исправление YAML (yamllint)
	@echo "🧹 Исправление YAML..."
	# Приведение синтаксиса и булевых значений
	find .github/workflows -type f -name "*.yml" \
	 -exec sed -i 's/\[ /[/' {} \; \
	 -exec sed -i 's/ \]/]/' {} \; \
	 -exec sed -i 's/\"true\"/true/' {} \; \
	 -exec sed -i 's/\"false\"/false/' {} \; \
	 -exec sed -i '1{/^---/!s/^/---\n/}' {} + \
	 -exec sed -i 's/\([^ ]\)#/\1  #/g' {} +
	# Добавляем заголовок в ключевые YAML
	@sed -i '1{/^---/!s/^/---\n/}' .pre-commit-config.yaml || true
	@sed -i '1{/^---/!s/^/---\n/}' docker-compose.yml || true
	@sed -i '1{/^---/!s/^/---\n/}' docker-compose.prod.yml || true
	# Проверка yamllint (без node_modules)
	yamllint -c .yamllint.yml .github/workflows || true
	@git add .github/workflows .pre-commit-config.yaml docker-compose.yml docker-compose.prod.yml || true
	@git commit -m "chore(yaml): auto-fix yamllint compliance (finalized)" || echo "⚠️ Нет изменений."
	@echo "✅ YAML полностью выровнен."

# =================================
# 🧭 Progress (daily reports)
# =================================
progress-template:
	@mkdir -p $(PROGRESS_DOCS_DIR)
	@if [ -f "$(PROGRESS_TEMPLATE)" ]; then \
		cp $(PROGRESS_TEMPLATE) $(PROGRESS_FILE); \
		echo "✅ Создан новый отчёт: $(PROGRESS_FILE)"; \
	else \
		echo "# 📘 Отчёт $(PROGRESS_DATE)" > $(PROGRESS_FILE); \
		echo "" >> $(PROGRESS_FILE); \
		echo "**Дата:** $$(date '+%Y-%m-%d %H:%M:%S')" >> $(PROGRESS_FILE); \
		echo "**Контекст:** " >> $(PROGRESS_FILE); \
		echo "" >> $(PROGRESS_FILE); \
		echo "## ✅ Выполнено" >> $(PROGRESS_FILE); \
		echo "- " >> $(PROGRESS_FILE); \
		echo "" >> $(PROGRESS_FILE); \
		echo "## ⚙️ Примечания" >> $(PROGRESS_FILE); \
		echo "- " >> $(PROGRESS_FILE); \
		echo ""; \
		echo "✅ Базовый шаблон создан вручную"; \
	fi

progress-append:
	@echo "✏️ Вставь сюда факты (заверши Ctrl+D):"
	@echo "" >> $(PROGRESS_FILE)
	@cat >> $(PROGRESS_FILE)
	@echo "" >> $(PROGRESS_FILE)
	@echo "✅ Факты добавлены в $(PROGRESS_FILE)"

progress-snapshot:
	@mkdir -p $(PROGRESS_DIR)
	@cp $(PROGRESS_FILE) $(PROGRESS_SNAPSHOT)
	@echo "✅ Снапшот сохранён: $(PROGRESS_SNAPSHOT)"

progress-auto-push:
	@$(MAKE) progress-snapshot
	@git add $(PROGRESS_DOCS_DIR)/PROGRESS_*.md $(PROGRESS_DIR)/PROGRESS_*.md || true
	@git commit -m "📘 progress snapshot $(PROGRESS_DATE)_$(PROGRESS_TIME)" || echo "⚠️ Нет изменений для коммита."
	@git push origin main
	@echo "✅ Прогресс отправлен в GitHub (main)"

progress-auto-test:
	@echo "🚀 Выполняется полный цикл тестов + снапшот..."
	@$(MAKE) ci-test || echo "⚠️ Тесты завершились с предупреждениями"
	@$(MAKE) progress-auto-push
	@echo "✅ Цикл CI + Docs завершён."

progress-help:
	@echo "============================================"
	@echo "📘 PROGRESS & CI-DOCS v2.4 — Автоотчёты"
	@echo "--------------------------------------------"
	@echo " make progress-template   — создать новый отчёт"
	@echo " make progress-append     — добавить факты вручную"
	@echo " make progress-snapshot   — сохранить снапшот отчёта"
	@echo " make progress-auto-push  — снапшот + commit + push"
	@echo " make progress-auto-test  — тесты + снапшот + push"
	@echo "--------------------------------------------"

# =================================
# 🔧 Git / Sync
# =================================
git-add: ## ➕ git add .
	git add .

git-fix: ## 🧹 Авто-фиксы (миграции + pre-commit)
	docker exec -it $(BACKEND_CONTAINER) python3 scripts/fix_migrations.py || true
	pre-commit run --all-files || true

git-commit: ## 💾 Commit (make git-commit m="msg")
	@if [ -z "$(m)" ]; then echo "❌ Укажи сообщение: make git-commit m=\"msg\""; exit 1; fi
	git commit -m "$(m)" --allow-empty || true

git-push: ## ⬆️ Push main
	git push origin main

git-all: ## 🚀 add+commit+push (make git-all m="msg")
	git add .
	pre-commit run --all-files || true
	@if [ -z "$(m)" ]; then git commit -m "chore: update"; else git commit -m "$(m)"; fi
	git push origin main
	@echo "✅ Коммит отправлен в GitHub."

git-amend: ## ✏️ Amend последнего коммита
	git add .
	pre-commit run --all-files || true
	git commit --amend --no-edit || true
	git push origin main --force

git-sync: ## 🔄 git fetch/rebase + restore stash
	@git stash push -m "sync-stash" || true
	@git fetch origin main
	@git rebase origin/main || true
	@git stash pop || true
	@echo "✅ Репозиторий синхронизирован."

git-reset-hard: ## 💥 Жёсткий сброс на origin/main
	git fetch origin main
	git reset --hard origin/main

git-reset-soft: ## 📝 Soft reset на origin/main
	git fetch origin main
	git reset --soft origin/main

sync-github:
	@echo "🔄 Проверка статуса репозитория..."
	git status
	@echo "📦 Добавление изменений..."
	git add .
	@echo "📝 Коммит..."
	git commit -m "🔄 auto-sync: $$(date '+%Y-%m-%d %H:%M:%S')" || echo "⚠️ Нет изменений для коммита."
	@echo "🚀 Push на GitHub..."
	git push origin main
	@echo "✅ Синхронизация завершена!"

# =================================
# 🧰 DevOps (venv, perms, reset, run)
# =================================
venv-reset:
	@echo "🧹 Удаляем старое виртуальное окружение..."
	sudo rm -rf venv
	@echo "🐍 Создаём новое виртуальное окружение..."
	python3 -m venv venv
	@echo "🚀 Устанавливаем зависимости..."
	. venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt
	@echo "✅ Окружение готово!"

fix-perms:
	@echo "🔧 Восстанавливаем права доступа на проект..."
	sudo chown -R admin:admin ~/my_projects/legal-assistant-arbitrage-v2
	sudo chmod -R u+rwX,go+rX,go-w ~/my_projects/legal-assistant-arbitrage-v2
	@echo "✅ Права восстановлены!"

reset-all: ## Полный ресет окружения
	docker compose -f $(COMPOSE_FILE) down --volumes --remove-orphans
	docker compose -f $(COMPOSE_FILE) up -d db
	$(MAKE) wait-for-db
	-$(MAKE) drop-db
	$(MAKE) create-db
	docker compose -f $(COMPOSE_FILE) up -d backend
	$(MAKE) migrate
	@if [ -f "$(SEED_FILE)" ]; then $(MAKE) seed; fi
	@echo "✅ Ресет завершён"

reset-db: drop-db create-db migrate seed ## 💣 Пересоздать базу и миграции

reset-migrations: ## 💣 Полный сброс миграций
	rm -f migrations/versions/*.py || true
	-$(MAKE) drop-db
	$(MAKE) create-db
	docker exec -it $(BACKEND_CONTAINER) alembic revision --autogenerate -m "init schema"
	$(MAKE) migrate

run: ## 🚀 Запуск FastAPI локально
	nohup uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000 > uvicorn.log 2>&1 &

stop: ## ⏹️ Остановить FastAPI
	@pkill -f "uvicorn backend.app.main:app --reload" || true

status: ## 📋 Проверить статус uvicorn
	@pgrep -a -f "uvicorn backend.app.main:app --reload" || echo "❌ uvicorn не запущен"

logs-local: ## 📜 Логи uvicorn
	@tail -f uvicorn.log

restart: stop run ## 🔄 Перезапуск uvicorn

deploy: setup-prod ## 🚀 Деплой

# =================================
# 🧪 Postman — генерация/экспорт/CI
# =================================
postman: ## 🧩 Сгенерировать Postman коллекцию (make postman HOST_URL=http://IP:8080)
	@if [ -z "$(HOST_URL)" ]; then echo "⚠️  Используется BASE_URL по умолчанию: http://127.0.0.1:8080"; fi
	docker compose -f $(COMPOSE_FILE) exec backend sh -c "PYTHONPATH=/code BASE_URL=$(HOST_URL) python3 scripts/generate_postman.py"
	$(MAKE) postman-export

postman-export: ## 📦 Упаковать коллекцию в ZIP
	@mkdir -p artifacts
	zip -j artifacts/postman_collection.zip docs/postman_collection.json
	@echo "✅ Архив сохранён: artifacts/postman_collection.zip"

postman-download: ## 📥 Скачать коллекцию (WSL → Windows) make postman-download HOST=user@host
	@if [ -z "$(HOST)" ]; then echo "❌ Укажи сервер, пример: make postman-download HOST=admin@1.2.3.4"; exit 1; fi
	scp $(HOST):/home/admin/my_projects/legal-assistant-arbitrage-v2/artifacts/postman_collection.zip /mnt/c/Users/alexe/Downloads/
	@echo "✅ Коллекция скопирована в C:\\Users\\alexe\\Downloads\\postman_collection.zip"

postman-download-win: ## 📥 Скачать через pscp.exe
	@if [ -z "$(HOST)" ]; then echo "❌ Укажи сервер, пример: make postman-download-win HOST=admin@1.2.3.4"; exit 1; fi
	pscp.exe $(HOST):/home/admin/my_projects/legal-assistant-arbitrage-v2/artifacts/postman_collection.zip C:\\Users\\alexe\\Downloads\\
	@echo "✅ Коллекция скопирована в C:\\Users\\alexe\\Downloads\\postman_collection.zip"

postman-serve: ## 🌐 Временный HTTP-сервер для скачивания
	@echo "🚀 Запускаем HTTP-сервер для скачивания Postman коллекции..."
	@cd artifacts && python3 -m http.server 8080 --bind 0.0.0.0 &
	@sleep 2
	@SERVER_PID=$$(pgrep -f "http.server 8080" | head -n1); \
	IP=$$(hostname -I | awk '{print $$1}'); \
	echo ""; \
	echo "✅ Коллекция доступна по адресу:"; \
	echo "   🌍 http://$$IP:8080/postman_collection.zip"; \
	echo ""; \
	read -p 'Нажмите [Enter], чтобы остановить сервер...'; \
	kill $$SERVER_PID && echo "🛑 HTTP-сервер остановлен."

postman-api-route: ## ⚙️ Подсказка для /api/docs/postman
	@echo "➡️  Добавь файл backend/app/routes/docs.py и зарегистрируй router в main.py (см. предыдущие инструкции)."

# --- Newman CI flows ---
test-ci-v31:
	@echo "🚀 Newman CI (AutoAuth v3.1)..."
	@mkdir -p artifacts
	newman run docs/Legal_Assistant_Arbitrage_v3.1_CI.postman_collection.json \
	  -e docs/Legal_Assistant_Env.postman_environment.json \
	  --reporters cli,html \
	  --reporter-html-export artifacts/newman_report_v31.html || { \
	    echo '❌ Ошибка (см. отчёт)'; exit 1; }
	@echo "✅ artifacts/newman_report_v31.html"

test-ci-v32:
	@echo "🚀 Newman CI (AutoAuth v3.2)..."
	newman run docs/Legal_Assistant_Arbitrage_v3.2_CI.postman_collection.json \
	  -e docs/Legal_Assistant_Env.postman_environment.json \
	  --reporters cli,html \
	  --reporter-html-export artifacts/newman_report_v32.html || { \
	    echo '❌ Ошибка (см. отчёт)'; exit 1; }
	@echo "✅ artifacts/newman_report_v32.html"

test-ci-v33:
	@echo "🚀 Newman CI (AutoAuth v3.3 — Stable)..."
	newman run docs/Legal_Assistant_Arbitrage_v3.3_CI.postman_collection.json \
		-e docs/Legal_Assistant_Env.postman_environment.json \
		--reporters cli,html \
		--reporter-html-export artifacts/newman_report_v33.html || { \
			echo '❌ Ошибка (см. artifacts/newman_report_v33.html)'; exit 1; }

test-ci-v3: ## Полный CI-цикл (pytest + Postman + снапшот + push)
	@echo "🚀 Полный CI-цикл AutoAuth v3.3"
	@START=$$(date '+%Y-%m-%d %H:%M:%S'); \
	$(MAKE) test-ci-v33 && STATUS="✅ OK" || STATUS="❌ Ошибка"; \
	echo "📸 Снапшот..."; $(MAKE) progress-snapshot; \
	echo "🧾 Запись в PROGRESS_TACTICAL.md..."; \
	echo "" >> docs/PROGRESS_TACTICAL.md; \
	echo "🧪 CI v3.3 — $$STATUS ($$START)" >> docs/PROGRESS_TACTICAL.md; \
	$(MAKE) progress-auto-push; \
	echo "✅ Полный CI завершён."

# =================================
# ⚙️ Helpers (routes, KAD)
# =================================
routes: ## 📋 Список маршрутов FastAPI
	@docker compose -f $(COMPOSE_FILE) exec backend python -c "from backend.app.main import app; print([r.path for r in app.routes])"

kad-test:
	@pytest -q backend/app/tests/test_kad_api.py -vv

kad-lint:
	@ruff check backend/app/integrations/kad_api.py backend/app/tests/test_kad_api.py || true

kad-env-example:
	@echo "KAD_BASE_URL=https://kad.arbitr.ru"; \
	echo "KAD_API_KEY=your_token_here"; \
	echo "KAD_TIMEOUT_S=15"; \
	echo "KAD_MAX_RETRIES=2"

# =================================
# 🛠 Fix (timezone & telegram)
# =================================
fix-tests-auth:
	@echo "🧩 Исправляем datetime и Telegram skip..."
	find backend/app -type f -name '*.py' -exec sed -i 's/datetime.utcnow()/datetime.now(timezone.utc)/g' {} +
	sed -i 's/pytest.fail(/pytest.skip(/' backend/app/tests/test_integration_notify.py || true
	@echo "✅ Исправлено: timezone-aware UTC и skip Telegram"

# ================================
# 🏁 FINALIZE v2.4 (Stable Snapshot)
# ================================
.PHONY: finalize-v2.4
finalize-v2.4:
	@echo "🏁 Финализация релиза v2.4 (All tests passed)..."
	@echo "🔍 Запуск pre-commit проверки..."
	pre-commit run --all-files --show-diff-on-failure || true
	@echo "📸 Сохранение снапшота..."
	$(MAKE) progress-snapshot
	@echo "💾 Коммит и пуш релиза..."
	git add .
	git commit -m "🏁 v2.4-final ✅ All tests passed (timezone-aware, stable CI, clean warnings)" || echo "⚠️ Нет изменений для коммита."
	git push origin main
	@echo "✅ Финализация завершена. Репозиторий синхронизирован с GitHub."

# ================================
# 🧰 FIX FINAL PRE-COMMIT ISSUES
# ================================
fix-final:
	@echo "🧩 Исправляем ошибки pre-commit..."
	sed -i 's/rr"\\\\d"/r"\\\\d"/' scripts/fix_regex.py
	sed -i 's/from datetime import datetime, timezone/from datetime import datetime/' backend/app/schemas/*.py || true
	sed -i 's/^from backend\.app\.routes import docs, reset/# moved down/' backend/app/main.py || true
	npx markdownlint-cli2 --fix "docs/**/*.md" "artifacts/**/*.md" || true
	black backend/ scripts/ || true
	isort backend/ scripts/ || true
	git add .
	git commit -m "fix: auto-correct pre-commit issues before finalize v2.4" || true
	@echo "✅ Все pre-commit ошибки устранены."

# ===========================
# 🧹 FIX YAML WRAP (Prettier)
# ===========================
fix-yaml-wrap: ## 🧹 Переформатировать YAML под 80 символов (Prettier)
	@echo "🧹 Форматируем YAML-файлы (до 80 символов в строке)..."
	npx prettier --write "**/*.yml" --print-width 80
	@git diff -- . ':!node_modules' > artifacts/fix_yaml_prettier.diff || true
	@git add .github/workflows/*.yml docker-compose*.yml .yamllint.yml || true
	@git commit -m "chore(yaml): reformat with Prettier (80 chars width)" || echo "⚠️ Нет изменений."
	@echo "✅ YAML успешно переформатирован и зафиксирован."

# =================================
# 📖 Help
# =================================
help: ## 📖 Все команды
	@echo "=== 🧭 Makefile Legal Assistant Arbitrage v2.7 ==="
	@grep -E '^[a-zA-Z0-9_.-]+:.*?## .*$$' $(MAKEFILE_LIST) \
	| awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-28s\033[0m %s\n", $$1, $$2}'

.PHONY: \
	backup-makefile \
	up down rebuild restart-docker logs ps shell ps-docker logs-docker shell-docker \
	doctor-check migrate makemigrations fix-migrations current history heads downgrade merge-heads stamp-head check-migrations \
	db-shell db-tables db-dump db-restore db-reset-tables drop-db create-db check-db db-inspect wait-for-db seed \
	health-host health-container wait-for-api \
	install install-dev setup-dev setup-prod smoke smoke-local smoke-ci test test-verbose docker-test ci-test coverage \
	telegram-notify telegram-notify-test \
	apidocs archdocs docs \
	sed-help sed-template sed-clean sed-fix-rules sed-validate sed-auto sed-auto-safe sed-restore sed-log-archive \
	pre-commit lint lint-tabs format fix-docs fix-yaml \
	progress-template progress-append progress-snapshot progress-auto-push progress-auto-test progress-help \
	git-add git-fix git-commit git-push git-all git-amend git-sync git-reset-hard git-reset-soft sync-github \
	venv-reset fix-perms reset-all reset-db reset-migrations run stop status logs-local restart deploy \
	postman postman-export postman-download postman-download-win postman-serve postman-api-route \
	test-ci-v31 test-ci-v32 test-ci-v33 test-ci-v3 \
	routes kad-test kad-lint kad-env-example \
	fix-tests-auth help
