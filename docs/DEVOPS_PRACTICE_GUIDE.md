# ⚙️ Legal Assistant Arbitrage v2 — DevOps Practice Guide

**Версия:** 2.4
\*\*Последнее обновление: 2025-10-13

---

## 🎯 1. Цель и концепция DevOps-практики

Цель DevOps-инфраструктуры — создать **самопроверяющийся CI/CD-поток**,
в котором качество, безопасность и единообразие контролируются автоматически.

> 🧠 DevOps — это культура автоматизации и ответственности:
> _«Каждый коммит проходит через весь цикл проверки, прежде чем попасть в продакшен.»_

---

## 🧩 2. Общая схема CI/CD Pipeline

```text
Commit → Pre-commit → CI (GitHub Actions) → Tests → AutoFix → Deploy → Notify
```

| Этап              | Назначение                           | Инструменты                              |
| ----------------- | ------------------------------------ | ---------------------------------------- |
| **Pre-commit**    | Локальная проверка и автоисправления | `pre-commit`, `flake8`, `isort`, `black` |
| **CI Tests**      | Автотестирование                     | `pytest`, `newman`                       |
| **Security Scan** | Поиск токенов и уязвимостей          | `detect-secrets`, `bandit`               |
| **Formatting**    | Унификация кода и документации       | `black`, `markdownlint`, `yamllint`      |
| **AutoFix**       | Автоматическое исправление и amend   | post-commit hook                         |
| **Deploy**        | Автодеплой из CI/CD                  | Docker Compose + GitHub Actions          |
| **Notify**        | Telegram-уведомления о статусе       | Bot API                                  |

---

## 🤖 3. Pre-commit хуки и автоформатирование

**Файл:** `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 25.9.0
    hooks:
      - id: black
        args: [--line-length=88]

  - repo: https://github.com/PyCQA/isort
    rev: 6.1.0
    hooks:
      - id: isort
        args: [--profile=black]

  - repo: https://github.com/pycqa/flake8
    rev: 7.3.0
    hooks:
      - id: flake8
        entry: flake8 --config=.flake8
        types: [python]

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v6.0.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-merge-conflict

  - repo: https://github.com/igorshubovych/markdownlint-cli
    rev: v0.45.0
    hooks:
      - id: markdownlint
        files: ^docs/
        args: [--config, .markdownlint.yaml]

  - repo: https://github.com/adrienverge/yamllint
    rev: v1.37.1
    hooks:
      - id: yamllint
        args: [-d, "{extends: default, rules: {line-length: disable}}"]

  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.5.0
    hooks:
      - id: detect-secrets
        args: [--baseline, .secrets.baseline]
```

📌 Все файлы проходят проверку до коммита, включая **Python**, **YAML** и **Markdown**.
Ошибки форматирования исправляются автоматически.

---

## ⚙️ 4. Auto-commit и post-fix логика

```yaml
- repo: local
  hooks:
    - id: auto-commit-after-fix
      name: Auto commit after pre-commit fixes
      entry: >
        bash -c '
        if git diff --quiet; then
          echo "[auto-commit] Nothing to fix.";
        else
          echo "[auto-commit] Fixed files found, amending commit...";
          git add -u && git commit --amend --no-edit || true;
        fi
        '
      language: system
      always_run: true
      stages: [post-commit]
```

🎯 Результат — разработчик видит только финальный «чистый» коммит,
даже если pre-commit внёс правки.

---

## 🔒 5. Безопасность и DevSecOps

| Контроль             | Средство                               | Цель                       |
| -------------------- | -------------------------------------- | -------------------------- |
| Secrets              | `detect-secrets` + `.secrets.baseline` | предотвращение утечек      |
| Static Code Analysis | `bandit`                               | поиск уязвимостей          |
| Env Isolation        | `.env`, Docker secrets                 | надёжное хранение токенов  |
| MFA / GitHub Secrets | включено                               | безопасность CI/CD-токенов |

---

## 🚀 6. GitHub Actions CI Pipeline

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:

jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run pre-commit hooks
        run: pre-commit run --all-files

      - name: Run pytest
        run: pytest --maxfail=1 --disable-warnings -q

      - name: Telegram notification
        if: always()
        run: |
          python backend/app/utils/notify_telegram.py "✅ CI complete for ${{ github.ref_name }}"
```

---

## 🧰 7. Makefile-команды

| Команда              | Описание                        |
| -------------------- | ------------------------------- |
| `make lint`          | flake8 + isort + black          |
| `make test`          | pytest                          |
| `make check-all`     | полный аудит проекта            |
| `make weekly-check`  | автоматическая проверка по cron |
| `make telegram-test` | тестовое уведомление            |

---

## 🧭 8. Автоматический аудит (weekly-check)

Еженедельная проверка выполняется через `cron`:

```
0 9 * * MON cd ~/my_projects/legal-assistant-arbitrage-v2 && make weekly-check >> ~/weekly.log 2>&1
```

Проверяется:

- `pre-commit run` на всех файлах
- актуальность `.secrets.baseline`
- Telegram-уведомление о статусе
- лог сохраняется в `artifacts/weekly_report.md`

---

## 📊 9. Метрики CI/CD-эффективности

| Метрика               | Цель   | Инструмент       |
| --------------------- | ------ | ---------------- |
| Pipeline success rate | 100 %  | GitHub Actions   |
| Lint compliance       | 100 %  | flake8, yamllint |
| Secrets scan pass     | 100 %  | detect-secrets   |
| AutoFix coverage      | ≥ 90 % | post-commit      |
| Docs style compliance | 100 %  | markdownlint     |

---

## 🧠 10. Принципы инженерной DevOps-культуры

- Commit small, test often — короткие циклы изменений.
- You break it — you fix it — общее владение кодом.
- Automate everything — ручное действие = баг.
- Shift left — ошибки ловятся до CI.
- Transparency first — пайплайны и метрики публичны.
- Security by design — безопасно по умолчанию.

---

## 🏁 11. Итог

Legal Assistant Arbitrage — пример самообслуживающегося DevOps-контура, где:

- каждая ошибка фиксируется автоматически,
- каждая метрика видна команде,
- каждая сборка безопасна и предсказуема.

💬 _«Automate what you fear, document what you trust.»_
— **Alex**, DevOps Lead, Legal Assistant Arbitrage v2

📅 Последняя ревизия: 2025-10-11
👤 Автор: Alex (admin@legal-assistant)

---

## 🧩 12. Управление патчами и снапшотами (v2.4)

Система патчей и снапшотов фиксирует текущее состояние кода и DevOps-инфраструктуры
для восстановления или анализа изменений.

### 🔧 Основные команды

| Команда                 | Назначение                                 |
| ----------------------- | ------------------------------------------ |
| `make snapshot-patches` | создаёт полный и секционный снимок системы |
| `make patch-check`      | проверяет применимость патчей (dry-run)    |
| `make patch-test`       | показывает статистику изменений            |
| `make patch-clean`      | очищает дубликаты, создаёт placeholders    |

### 🗂️ Структура каталогов

```text
patches/
├── _archive/              # архивные снапшоты
├── old/                   # устаревшие или экспериментальные патчи
├── v2.4_devops_docs_HEAD.patch
├── v2.4_scripts_HEAD.patch
└── v2.4_full_snapshot_YYYYMMDD_HHMM.patch
```

### 🧾 Автоматизация

- Каждый `snapshot-patches` логируется в:
  - `artifacts/WEEKLY_AUDIT_YYYYMMDD.md`
  - `artifacts/patch_audit_YYYYMMDD_HHMM.log`

- Архив снапшотов сохраняется в `artifacts/patches_snapshot_YYYYMMDD_HHMM/`.

### 💡 Практика

- Запускать перед релизом или после успешного CI.
- Хранить папку `patches/` в репозитории.
- Пустые `.patch`-файлы допустимы (placeholders для структуры).
- Для отката можно применить нужный патч:

```bash
git apply patches/v2.4_full_snapshot_20251012_1641.patch
```

---

📅 Раздел добавлен в версии 2.4 (патч-workflow автоматизирован).
👤 Ответственный: Alex (admin@legal-assistant)

---
