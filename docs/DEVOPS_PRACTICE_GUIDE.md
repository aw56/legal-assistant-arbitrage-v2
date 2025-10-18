---

### 🔹 Этап 1 из 4

**Файл:** `docs/DEVOPS_PRACTICE_GUIDE.md`
**Версия:** `v2.9.7`
**Цель:** Полная синхронизация с CI Pipeline Guide, интеграционный alias-слой (`app.integrations.*`), новый Clean Protocol v2.9.7.
**Принцип:** без потерь — сохраняем твою структуру, добавляем уточнения, связываем с тестовым и CI-контуром.

---

````markdown
# ⚙️ Legal Assistant Arbitrage v2 — DevOps Practice Guide

**Версия:** 2.9.7
**Последнее обновление:** 2025-10-16

---

## 🎯 1. Цель и концепция DevOps-практики

DevOps-контур проекта Legal Assistant Arbitrage v2.9.7 представляет собой **самоподдерживающуюся экосистему**:
всё — от коммита до Telegram-уведомления — работает через автоматизацию и обратную связь.

> 🧠 DevOps — это контроль, прозрачность и воспроизводимость.
> «Каждый коммит проходит путь: _анализ → тест → снапшот → уведомление_.»

---

## 🧩 2. CI/CD Pipeline (v2.9.7 Clean Protocol)

```text
Commit → Pre-commit → Lint/Test → CI AutoAuth → Integration Layer → Deploy → Notify
```
````

| Этап                  | Назначение                             | Инструменты / Автоматизация                |
| --------------------- | -------------------------------------- | ------------------------------------------ |
| **Pre-commit**        | Локальная проверка и автоисправления   | black · isort · flake8 · markdownlint      |
| **CI AutoAuth**       | Тестовый прогон Postman + Newman       | AutoAuth v3.3                              |
| **Integration Tests** | Проверка alias-импортов и внешних API  | pytest -m integration                      |
| **Security Scan**     | Контроль токенов и конфигураций        | detect-secrets · bandit                    |
| **Snapshot System**   | Создание снапшотов проекта после CI    | make snapshot-patches + progress-auto-push |
| **Deploy & Notify**   | CI-деплой Docker и Telegram-оповещения | GitHub Actions + Bot API                   |

---

## 🧠 3. Архитектура Import Alias (Integration Layer)

В версии **v2.9.7** добавлен alias-механизм:

```python
import backend.app.integrations.integration_logger as direct
import app.integrations.integration_logger as alias
```

**Назначение:**

- pytest видит `backend.app.*` при запуске из корня,
- продакшн и Postman используют короткий алиас `app.*`,
- IDE-подсветка одинакова в обоих контекстах.

**Реализация:** `backend/app/integrations/__init__.py`

```python
import sys, importlib
_real_pkg = "backend.app.integrations"
for submod in ("integration_logger", "base_service"):
    module = importlib.import_module(f"{_real_pkg}.{submod}")
    sys.modules[f"app.integrations.{submod}"] = module
```

🧩 Проверка:

```bash
Aliased is direct: True
log_integration_event: True
```

---

## 🧾 4. Pre-commit Hooks Chain (v2.9.7)

Файл: `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 25.9.0
    hooks: [{ id: black, args: [--line-length=88] }]
  - repo: https://github.com/PyCQA/isort
    rev: 6.1.0
    hooks: [{ id: isort, args: [--profile=black] }]
  - repo: https://github.com/pycqa/flake8
    rev: 7.3.0
    hooks: [{ id: flake8, entry: flake8 --config=.flake8 }]
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v6.0.0
    hooks: [{ id: trailing-whitespace }, { id: end-of-file-fixer }, { id: check-yaml }, { id: check-json }]
  - repo: https://github.com/igorshubovych/markdownlint-cli
    rev: v0.45.0
    hooks: [{ id: markdownlint, files: ^docs/ }]
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.5.0
    hooks: [{ id: detect-secrets, args: [--baseline, .secrets.baseline] }]
```

---

## ⚙️ 5. Auto-Fix и Post-Commit Logic

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
          echo "[auto-commit] Amending fixed commit...";
          git add -u && git commit --amend --no-edit || true;
        fi
        '
      language: system
      stages: [post-commit]
```

💡 При стабильной конфигурации можно снова включить этот хук (по умолчанию в 2.9.7 он отключён в `.pre-commit-config.yaml` для предотвращения рекурсии).

---

## 🔒 6. DevSecOps и защита CI/CD

| Контроль                 | Средство                | Цель                        |
| ------------------------ | ----------------------- | --------------------------- |
| Secrets Baseline         | detect-secrets          | предотвращение утечек       |
| Static Code Analysis     | bandit                  | анализ уязвимостей          |
| Docker Secrets Isolation | docker-compose.prod.yml | безопасная передача токенов |
| GitHub Secrets / MFA     | Actions + 2FA           | защита токенов CI           |

---

## 🧪 7. Integration Layer Tests

| Модуль                       | Назначение                        |
| ---------------------------- | --------------------------------- |
| `test_integration_logger.py` | Проверка записи логов             |
| `test_base_service.py`       | Проверка HTTP-логики и mock-сетей |
| `test_integration_notify.py` | Telegram-уведомления              |

✅ Состояние v2.9.7:

```
pytest -m integration → 8 passed, 0 failed
```

---

## 🚀 8. GitHub Actions Workflow

```yaml
name: CI
on:
  push:
    branches: [main]
jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: pip install -r requirements.txt
      - run: pre-commit run --all-files
      - run: pytest -m integration --disable-warnings -q
      - run: python backend/app/utils/notify_telegram.py "✅ CI complete for ${{ github.ref_name }}"
```

---

## 🧰 9. Makefile Essentials

| Команда                   | Описание                        |
| ------------------------- | ------------------------------- |
| `make test`               | Запуск pytest                   |
| `make integration-local`  | Интеграционные тесты с Telegram |
| `make progress-auto-push` | Снапшот + пуш                   |
| `make patch-check`        | Проверка патчей                 |
| `make weekly-check`       | Автоматическая проверка среды   |

---

## 📊 10. CI/CD Метрики

| Метрика                | Цель  | Инструмент           |
| ---------------------- | ----- | -------------------- |
| Lint compliance        | 100 % | flake8, markdownlint |
| Integration tests pass | 100 % | pytest, respx        |
| Secrets scan           | 100 % | detect-secrets       |
| CI success rate        | 100 % | GitHub Actions       |
| Docs style compliance  | 100 % | markdownlint-cli     |

---

## 📘 11. Snapshot & Patch Management

**make snapshot-patches** — полный снимок проекта (v2.9.7).

Пример структуры:

```
patches/
├── v2.9_integration_alias.patch
├── v2.9_docs_baseline.patch
└── v2.9_full_snapshot_20251016_1048.patch
```

---

## 🧠 12. Культура DevOps-инженерии

- Automate everything — ручное действие = риск.
- You break it — you fix it — коллективная ответственность.
- Shift left — ошибки ловим до CI.
- Security by design — безопасность встроена.
- Transparency first — метрики и логи открыты.

---

## 🏁 13. Итог

Legal Assistant Arbitrage v2.9.7 — **чистая, самопроверяющаяся DevOps-архитектура**:

✅ Все тесты зелёные
✅ Pre-commit изолирует ошибки
✅ Snapshot-система сохраняет состояние
✅ Telegram сообщает о каждом этапе

> 💬 «Automate what you fear, document what you trust.»
> — **Aleksej**, автор и DevOps-архитектор проекта

📅 Ревизия: 2025-10-16
👤 Ответственный: **Alex (admin@legal-assistant)**

```

---
```
