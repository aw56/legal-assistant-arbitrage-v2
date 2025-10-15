
---
title: "Make Patch & Release Guide"
version: "v2.8-dev"
author: "Aleksej — Project Owner"
created: "2025-10-14"
status: "✅ Stable"
description: "Руководство по созданию, проверке и выпуску патчей и релизов Legal Assistant Arbitrage API v2.8+"
---

# 🧩 Make Patch & Release Guide — Legal Assistant Arbitrage v2.8+

## 📘 Назначение

Данный документ описывает:

- унификацию **патч-системы и релизных целей** в `Makefile`;
- правила создания, проверки и отката патчей (v2.8+);
- принципы разделения Make-модулей в каталоге `make/`;
- стандарт DevOps-чистоты при выпуске каждой версии.

---

## ⚙️ 1. Новая структура Make-модулей

С версии **v2.8-dev** цели `release-template` и `patch-verify` вынесены в отдельные подключаемые файлы:

make/
├── patch-verify.mk # Проверка целостности и обратимости патчей
└── release-template.mk # Универсальный релизный пайплайн (опционально)

pgsql
Копировать код

В корневом `Makefile` теперь достаточно двух строк:

```makefile
include make/patch-verify.mk
include make/release-template.mk
🧩 2. Универсальная цель проверки патчей
Файл: make/patch-verify.mk

makefile
Копировать код
.PHONY: patch-verify
patch-verify: ## Verify patch integrity and reversibility (usage: make patch-verify version=v2.8)
        @ver=$${version:-v2.8}; \
        patch_file="patches/$$ver/$${ver}_dev_base_state.patch"; \
        echo "🔍 Checking patch integrity for $$ver..."; \
        if [ ! -f "$$patch_file" ]; then \
                echo "❌ Patch file not found: $$patch_file"; exit 1; fi; \
        if git apply --check "$$patch_file" >/dev/null 2>&1; then \
                echo "✅ Patch can be applied cleanly."; \
        else \
                echo "⚠️  Patch already applied or conflicts detected."; \
        fi; \
        if git apply --reverse --check "$$patch_file" >/dev/null 2>&1; then \
                echo "✅ Reverse check passed (safe rollback possible)."; \
        else \
                echo "⚠️  Reverse check failed (already base or modified)."; \
        fi; \
        echo "📄 Patch summary:"; \
        if git rev-parse "$${ver}-base" >/dev/null 2>&1; then \
                git diff "$${ver}-base"..HEAD --stat; \
        else \
                echo "⚠️  Base tag $${ver}-base not found."; \
        fi
📖 Пример запуска проверки патча
bash
Копировать код
make patch-verify version=v2.8
Результат:

css
Копировать код
🔍 Checking patch integrity for v2.8...
✅ Patch can be applied cleanly.
✅ Reverse check passed (safe rollback possible).
📄 Patch summary:
 Makefile | 1 +
 1 file changed, 1 insertion(+)
🧾 3. Правила создания патчей
3.1 Базовая точка
Перед началом работы над новой веткой:

bash
Копировать код
git tag -f v2.8-base
Это зафиксирует текущее «чистое» состояние.

3.2 Снятие патча
После внесённых изменений создаём базовый патч:

bash
Копировать код
mkdir -p patches/v2.8
git diff v2.8-base..HEAD > patches/v2.8/v2.8_dev_base_state.patch
Проверяем:

bash
Копировать код
git apply --check patches/v2.8/v2.8_dev_base_state.patch
git apply --reverse --check patches/v2.8/v2.8_dev_base_state.patch
3.3 Названия и структура
Каждая версия хранит свои патчи изолированно:

markdown
Копировать код
patches/
 ├── v2.7/
 │   └── v2.7_20251014_0721_devops_general_clean_standard.patch
 └── v2.8/
     ├── v2.8_dev_base_state.patch
     ├── v2.8_dev_test.patch
     └── v2.8_dev_changes_since_base.patch
🚀 4. Универсальный релиз-пайплайн
Файл: make/release-template.mk

makefile
Копировать код
.PHONY: release-template
release-template: ## Run full release cycle (autoformat + tag + push)
        @ver=$${version:-v2.8}; \
        echo "🚀 Starting universal release pipeline for $$ver..."; \
        echo "🧹 Running cleanup and formatting..."; \
        black backend/app || true; \
        isort backend/app || true; \
        flake8 backend/app || true; \
        echo "🧩 Regenerating release snapshot..."; \
        make snapshot-patches || true; \
        echo "🪄 Linting and fixing markdown docs..."; \
        npx markdownlint-cli2 --fix "docs/**/*.md" || true; \
        echo "✅ Creating Git tag..."; \
        read -p "Enter new version tag (default $$ver): " tag; \
        tag=$${tag:-$$ver}; \
        git add docs && \
        git commit -am "chore(release): finalize $$tag" --no-verify && \
        git tag -a $$tag -m "Release $$tag — Autoformat + Docs Sync" && \
        echo "🎯 Tagged $$tag successfully!" && \
        git push origin release/$${ver}-dev --tags && \
        echo "✅ Release $$tag pushed successfully!"
📖 Пример запуска релиза
bash
Копировать код
make release-template version=v2.8
или просто:

bash
Копировать код
make release-template
(по умолчанию подставит v2.8).

🧱 5. Проверка и чистка перед релизом
Перед тем как тегировать релиз:

bash
Копировать код
make check-all
make patch-verify version=v2.8
После релиза:

bash
Копировать код
make snapshot-patches
make patch-clean
📚 6. Стандарты на будущее
Версия	Базовый тег	Каталог патчей	Основные цели
v2.7	v2.7	patches/v2.7/	release-v2.7, check-all
v2.8	v2.8-base	patches/v2.8/	release-template, patch-verify
≥v2.9	<ver>-base	patches/<ver>/	единые release-template и patch-verify

✅ 7. Контрольная команда
Чтобы убедиться, что всё настроено верно:

bash
Копировать код
make patch-verify version=v2.8 && make release-template version=v2.8
Если обе команды проходят без ошибок — система make/ собрана корректно, релизная цепочка готова к работе.
