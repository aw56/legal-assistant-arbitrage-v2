---
title: "Release CI Flow — Legal Assistant Arbitrage v2.9"
version: "v2.9"
author: "Aleksej — Project Owner"
created: "2025-10-17"
status: "✅ Active"
description: "CI/CD релизный поток: автоматическая сборка, проверка и деплой (v2.9+)"
---

# ⚙️ Release CI Flow — Legal Assistant Arbitrage v2.9

## 📘 Назначение

Документ описывает **автоматизированную релизную последовательность**,  
которая используется в GitHub Actions для Legal Assistant Arbitrage API начиная с версии **v2.9**.  
Все шаги выполняются без ручного вмешательства и проходят полную DevOps-валидацию.

---

## 🧩 1. Общая структура CI-потока

```text
push → collaboration-check → release-template → release-finalize → deploy → telegram-notify
Этап	Описание	Скрипт/Цель
1️⃣ Проверка среды	Полный аудит кода, docs, secrets	make collaboration-check
2️⃣ Формирование релиза	Генерация снапшота и релизного тега	make release-template
3️⃣ Архивация артефактов	Snapshot + patch-bundle в artifacts/	make release-finalize
4️⃣ Деплой (Docker)	CI-развёртывание на staging/prod	.github/workflows/deploy.yml
5️⃣ Telegram уведомление	Отправка отчёта о релизе	notify_telegram.py

🔄 2. Пример GitHub Actions (ci_release.yml)
yaml
Копировать код
name: Release CI
on:
  push:
    branches: [main, release/v2.9-dev]

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Verify environment
        run: make collaboration-check

      - name: Build release snapshot
        run: make release-template version=v2.9

      - name: Finalize release
        run: make release-finalize version=v2.9

      - name: Deploy (staging)
        run: docker compose -f docker-compose.prod.yml up -d

      - name: Telegram notify
        if: always()
        run: python backend/app/utils/notify_telegram.py "🚀 Release v2.9 completed!"
🧰 3. Локальное тестирование CI-процесса
Перед пушем в main можно проверить CI-цепочку вручную:

bash
Копировать код
make collaboration-check
make release-template version=v2.9
make release-finalize version=v2.9
Если все проверки проходят без ошибок — CI-поток завершится успешно и релиз будет зафиксирован на GitHub.

📦 4. CI-артефакты
Артефакт	Назначение
artifacts/newman_report_v3x.html	Отчёт AutoAuth
artifacts/integration_report.html	Отчёт интеграций
artifacts/patches_snapshot_*.md	История релизных снапшотов
artifacts/release_log_v2.9.txt	Лог CI-релиза
docs/RELEASE_OPERATIONS_GUIDE_v2.9.md	Основное руководство по релизам

🧠 5. Принципы CI-релизов
Все CI-запуски идемпотентны — повторный запуск не ломает окружение.

Любой релиз-тег (v2.9.x) создаётся автоматически и пушится в GitHub.

Telegram уведомления формируются в конце пайплайна.

Логи CI сохраняются локально и в артефактах GitHub Actions.

Все проверки (flake8, markdownlint, yamllint, pytest) обязательны.

🧩 6. Интеграция с Full Archive Mode
Этот документ является составной частью Full Archive-пакета (v2.9.7+).
Он синхронизирован с файлами:

docs/RELEASE_OPERATIONS_GUIDE_v2.9.md

make/release-template.mk

make/collaboration-check.mk

.github/workflows/ci_release.yml

🏁 7. Итог
CI-релиз выполняется полностью автоматически.

Все шаги воспроизводимы и прозрачны.

Telegram уведомление гарантирует контроль завершения.

После завершения все артефакты доступны в artifacts/.

📅 Последняя ревизия: 2025-10-17
👤 Ответственный: Aleksej (Project Owner)
🔗 Связан с: RELEASE_OPERATIONS_GUIDE_v2.9.md, COLLABORATION_STANDARD_v2.9.7.md

```
