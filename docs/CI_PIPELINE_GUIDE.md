---

````markdown
# 🧩 CI/CD Pipeline Guide — Legal Assistant Arbitrage v2.9.7

**Дата:** 2025-10-16
**Версия:** 2.9.7 Integration & Control Layer
**Автор:** Alex (admin@legal-assistant)

---

## 🎯 1. Назначение

Документ описывает **полный цикл CI/CD-конвейера** Legal Assistant Arbitrage v2.9.7:
от локальных хуков и pytest-проверок до автоснапшотов, деплоя и Telegram-уведомлений.

---

## ⚙️ 2. Общая схема потока

```text
Developer Commit
    ↓
Pre-commit (black · isort · flake8 · detect-secrets)
    ↓
GitHub Actions (CI + pytest + newman)
    ↓
Integration Stage (Telegram · KAD · Pravo)
    ↓
Snapshot → Deploy → Notify
```

| Этап               | Цель                                | Инструменты                           |
| ------------------ | ----------------------------------- | ------------------------------------- |
| Pre-commit         | Форматирование и проверка стиля     | black · isort · flake8 · markdownlint |
| Unit-tests         | Проверка основных эндпоинтов API    | pytest -m smoke                       |
| Integration Tests  | KAD / Pravo / Telegram              | pytest -m integration + AutoAuth v3.3 |
| Static Security    | Поиск уязвимостей и токенов         | detect-secrets · bandit               |
| Docs Check         | Стиль Markdown/YAML                 | markdownlint · yamllint               |
| Snapshot & Archive | Фиксация результатов в artifacts/   | Makefile + patches/ + git commit      |
| CI Notify          | Уведомление о результатах пайплайна | Bot API + httpx                       |

---

## 🧠 3. Pre-commit и локальный аудит

```bash
make verify-before-change
```

Запускает:

- `pre-commit run --all-files`
- `pytest -m smoke`
- `black isort flake8`
- `markdownlint docs/`

Отчёт сохраняется в `artifacts/PRECOMMIT_REPORT.md`.

---

## 🧪 4. Pytest и интеграционные тесты

**Быстрые тесты:**

```bash
pytest -m smoke --disable-warnings -q
```

**Полные интеграции (AutoAuth + Telegram):**

```bash
pytest -m integration -v --disable-warnings --maxfail=3
```

🟢 Результат v2.9.7 — 8/8 passed.
Логи → `artifacts/pytest_report.html`, `logs/integrations/`.

---

## 🧰 5. Makefile CI-команды

| Команда                   | Назначение                          |
| ------------------------- | ----------------------------------- |
| `make smoke-local`        | Локальные smoke-тесты + уведомление |
| `make integration-local`  | Интеграции (KAD/Pravo/Telegram)     |
| `make progress-auto-push` | Автоснапшот и пуш в GitHub          |
| `make ci-test`            | Полный CI-цикл (pytest + newman)    |
| `make check-all`          | Комплексная проверка перед пушем    |

Все отчёты → `artifacts/` (`newman_report_v33.html`, `PROGRESS_*.md`).

---

## 🔄 6. Newman + AutoAuth v3.3

Коллекция:

```
docs/Legal_Assistant_Arbitrage_v3.3_CI.postman_collection.json
```

Запуск:

```bash
newman run docs/Legal_Assistant_Arbitrage_v3.3_CI.postman_collection.json \
  -e docs/Legal_Assistant_Env.postman_environment.json \
  --reporters cli,html \
  --reporter-html-export artifacts/newman_report_v33.html
```

AutoAuth автоматически:
1️⃣ логинится в `/api/auth/login`;
2️⃣ создаёт временного пользователя;
3️⃣ прогоняет CRUD (`/laws`, `/decisions`, `/health`);
4️⃣ шлёт итог в Telegram.

---

## 🧩 7. GitHub Actions Workflow (v2.9.7)

```yaml
name: CI-Pipeline
on:
  push:
    branches: [main]

jobs:
  build-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - name: Install
        run: pip install -r requirements.txt
      - name: Run pre-commit
        run: pre-commit run --all-files
      - name: Run pytest
        run: pytest -m "smoke or integration" -v --disable-warnings
      - name: Run newman
        run: make ci-test
      - name: Telegram notify
        if: always()
        run: |
          python backend/app/utils/notify_telegram.py \
          "✅ CI завершён для ${{ github.ref_name }}"
```

---

## 🧱 8. DevSecOps-гейт

| Проверка        | Инструмент     | Действие при сбое            |
| --------------- | -------------- | ---------------------------- |
| Secret scan     | detect-secrets | блокировка коммита           |
| Static analysis | bandit         | предупреждение в CI          |
| Lint & Format   | flake8/black   | автоисправление pre-commitом |
| Markdown lint   | markdownlint   | отчёт в artifacts/           |

---

## 📊 9. Метрики пайплайна

| Метрика            | Цель (%) | Источник отчёта      |
| ------------------ | -------- | -------------------- |
| Успех CI           | 100      | GitHub Actions       |
| Покрытие тестами   | ≥ 95     | pytest / html-report |
| Секреты утечки     | 0        | .secrets.baseline    |
| Стиль документации | 100      | markdownlint summary |
| AutoFix coverage   | ≥ 90     | pre-commit лог       |

---

## 🚀 10. Снапшоты и релизы

```bash
make progress-auto-push
```

Создаются:

- `docs/PROGRESS_YYYYMMDD_HHMM.md`
- `artifacts/newman_report_v33.html`
- `patches/v2.9_full_snapshot_YYYYMMDD_HHMM.patch`

Релизы тегируются `v2.9.YYYYMMDD`.

---

## 📬 11. Telegram-уведомления

**Модуль:** `backend/app/utils/notify_telegram.py`

Примеры:

```
✅ CI complete for main
⚠️ Integration tests failed
📦 Snapshot created: PROGRESS_20251016_1030.md
```

---

## 🏁 12. Заключение

Legal Assistant Arbitrage v2.9.7 — самопроверяющийся CI/CD-контур:

- Все тесты и линт-проверки выполняются автоматически.
- Каждый CI фиксирует снапшот и шлёт уведомление.
- Безопасность и повторяемость встроены в архитектуру.

💬 _«Стабильность — результат дисциплины, а не удачи.»_

📅 Ревизия: 2025-10-16
👤 Автор: Aleksej (admin@legal-assistant)

```

---
```
