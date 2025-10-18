---
title: "Dependency Map — Legal Assistant Arbitrage v2.9.7"
version: "v2.9.7"
author: "Aleksej — Project Owner"
created: "2025-10-16"
status: "✅ Stable"
description: "Полная карта зависимостей проекта Legal Assistant Arbitrage v2.9.7 (Full Clean Chain)."
---

# 🧩 Legal Assistant Arbitrage v2.9.7 — Dependency Map (Full Clean Chain)

## 📘 Назначение

Документ фиксирует иерархию всех зависимостей DevOps-цепочки проекта  
— от исходного кода до CI/CD и документации, обеспечивая **чистоту, предсказуемость и контроль** над каждым изменением.

---

## 🧠 1. Общая структура зависимостей

bash
Копировать код
┌────────────────────────────┐
│ Makefile (Core) │
│────────────────────────────│
│ make check-all │
│ make verify-before-change │
│ make safe-push │
│ make progress-auto-push │
│ make collaboration-check │
└─────────────┬──────────────┘
│
▼
┌──────────────────────────────────────────────────────────────┐
│ Pre-commit Hooks Suite │
│──────────────────────────────────────────────────────────────│
│ black → isort → flake8 → markdownlint → yamllint → detect-secrets │
│ pytest (pre-push) │
└─────────────┬────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────┐
│ .flake8 Config │
│─────────────────────────────────────────────────────────────│
│ max-line-length=160 │
│ ignore: E203,E266,E501,W503,F403,F401 │
│ per-file-ignores: **init**.py, conftest.py:E402 │
└─────────────┬───────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────┐
│ Lint Pipeline │
│─────────────────────────────────────────────────────────────│
│ black/isort/flake8 → backend/app/**/\*.py │
│ markdownlint → docs/**/_.md │
│ yamllint → _.yml, .github/workflows/_.yml │
└─────────────┬───────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────┐
│ Test Layer │
│─────────────────────────────────────────────────────────────│
│ pytest.ini → rootdir=. , markers: smoke, integration │
│ backend/app/tests/conftest.py → test DB + fixtures │
│ test*integration*_ → Integration Layer checks │
│ test_smoke_health.py → API health test │
└─────────────┬───────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────┐
│ Integration Layer │
│─────────────────────────────────────────────────────────────│
│ backend/app/integrations/base_service.py │
│ backend/app/integrations/kad_service.py │
│ backend/app/integrations/pravo_service.py │
│ backend/app/integrations/integration_logger.py │
│ → ведёт логи в logs/integrations.log │
└─────────────┬───────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────┐
│ CI/CD Layer │
│─────────────────────────────────────────────────────────────│
│ .github/workflows/ci.yml → full test & lint │
│ .github/workflows/ci_integrations.yml → KAD/Pravo pipeline │
│ .github/workflows/docs.yml → Markdown validation │
│ ci_kad.yml, backup.yml, apidocs.yml │
└─────────────┬───────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────┐
│ Documentation Suite │
│─────────────────────────────────────────────────────────────│
│ docs/COLLABORATION_STANDARD_v2.9.7.md │
│ docs/MAKE_PATCH_AND_RELEASE_GUIDE_v2.8.md │
│ docs/SAFE_PUSH_AND_VERIFICATION_GUIDE_v2.8.md │
│ docs/ROADMAP_v2.9.md │
│ docs/INTEGRATION_REPORT_v2.9.7.html │
│ docs/DEVOPS_PRACTICE_GUIDE_v2.9.md │
└─────────────┬───────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────┐
│ Artifacts & Snapshots │
│─────────────────────────────────────────────────────────────│
│ artifacts/newman_report_v33.html │
│ artifacts/integration_report.html │
│ artifacts/PROGRESS_YYYYMMDD_HHMM.md │
│ logs/integrations.log │
└─────────────┬───────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────┐
│ CI AutoAuth v3.3 │
│─────────────────────────────────────────────────────────────│
│ Postman tests → newman HTML reports │
│ AutoAuth script for CI token injection │
│ Linked to GitHub Actions workflow via `make ci-test` │
└─────────────────────────────────────────────────────────────┘
yaml
Копировать код

---

## 🧭 2. Объяснение логики потоков

| Поток                  | Начало                   | Завершение                            | Цель                         |
| ---------------------- | ------------------------ | ------------------------------------- | ---------------------------- |
| **Code Clean Flow**    | black → isort → flake8   | Makefile / pre-commit                 | Синтаксис и стиль            |
| **Docs Clean Flow**    | markdownlint → yamllint  | Makefile / CI docs.yml                | Документация и YAML          |
| **Security Flow**      | detect-secrets           | pre-commit                            | Проверка токенов             |
| **Integration Flow**   | pytest -m integration    | artifacts/integration_report.html     | Проверка KAD / Pravo         |
| **Collaboration Flow** | make collaboration-check | docs/COLLABORATION_STANDARD_v2.9.7.md | Гарантия чистоты координации |
| **Release Flow**       | make release-template    | patches/v2.9/\*.patch + git tag       | Автоматизация релиза         |

---

## ⚙️ 3. Правило “Full Clean File Body”

Каждый файл в проекте обязан быть:

1. Полностью самодостаточным (`EOF`-закрытый блок при генерации).
2. Валиден по `markdownlint`, `yamllint`, `flake8`.
3. Готов к вставке через `cat > file <<'EOF' ... EOF`.
4. Содержать YAML-front-matter с полями:
   - `title`, `version`, `author`, `created`, `status`, `description`.
5. Проходить pre-commit без автоматических правок.

---

## 🧩 4. Контекстная логика

Перед каждым генеративным циклом:

1. Анализируется **полная карта зависимостей** (`код → тесты → документация → CI → make`).
2. Вычисляются все связанные файлы, затрагиваемые изменением.
3. Генерируется **единый архив-блок**, включающий:
   - `.py` — код;
   - `.md` — документацию;
   - `.yml` — конфиги;
   - при необходимости тесты и CI-фрагменты.

🧭 **Формула работы:**

> Один запрос → один чистый архив-блок → 100% lint-safe результат.

📌 Таким образом:

- тебе не нужно ловить файлы по частям;
- каждый релизный или интеграционный цикл идёт в один проход;
- ни один файл не ломает пайплайн (`markdownlint`, `yamllint`, `flake8`, `pytest`, `pre-commit` — всё проходит).

---

## 🧰 5. Проверка согласованности цепочки

Запусти:

```bash
make collaboration-check
Она выполняет:

Этап	Проверка	Инструмент
1	Markdown	markdownlint-cli2 "docs/**/*.md"
2	YAML	yamllint .
3	Python	flake8 backend
4	Smoke	pytest -m smoke -q
5	Collaboration file	grep -q "Full Archive Mode" docs/COLLABORATION_STANDARD_v2.9.7.md

📜 6. Итог
Всё в системе теперь взаимосвязано по принципу
«один поток — одна цель — одна точка входа».

✅ Любое изменение проходит:
lint → test → docs → CI → snapshot → release
без потери чистоты и воспроизводимости.

📅 Последняя ревизия: 2025-10-16
👤 Ответственный: Aleksej (Project Owner)

```
