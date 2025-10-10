Отлично ⚙️
Ты собрал идеальную DevOps-документацию для проекта —
и теперь вот финальный штрих: **единый сводный документ `docs/DEVOPS_HANDBOOK.md`**.

Он объединяет всё в одном месте, с навигацией, ссылками на каждый раздел, краткими аннотациями
и удобным оглавлением. Этот файл можно считать **официальным техническим DevOps-паспортом проекта**
**Legal Assistant Arbitrage v2.4**.

---

```markdown
# 🧭 DEVOPS HANDBOOK — Legal Assistant Arbitrage v2.4

## ⚖️ Введение

Добро пожаловать в **DevOps Handbook проекта Legal Assistant Arbitrage v2.4**.  
Этот документ объединяет все DevOps-руководства, инструкции, шаблоны и процессы,  
используемые в CI/CD, тестировании, деплое и обслуживании системы.

---

## 📚 Оглавление

1. [CI/CD Pipeline Overview](#-cicd-pipeline-overview)
2. [Test Guide](#-test-guide)
3. [DevOps Operations Manual](#-devops-operations-manual)
4. [Deploy Manual](#-deploy-manual)
5. [Rollback Manual](#-rollback-manual)
6. [Deploy Log Template](#-deploy-log-template)
7. [Appendix: DevOps Principles](#-appendix-devops-principles)

---

## 🚀 CI/CD Pipeline Overview

**Документ:** [`docs/CI_PIPELINE.md`](./CI_PIPELINE.md)

**Основные функции пайплайна:**

- Автоматический запуск при `push` или `pull_request`
- Этапы:
  1. 🧹 `lint-and-test` — проверка кода и миграций
  2. 🚦 `smoke` — проверка здоровья API
  3. 🧩 `integration` — тест внешних сервисов (Telegram и KAD)
  4. 🐳 `build-and-push` — сборка и публикация Docker-образа
  5. 🚀 `deploy` — деплой на staging или production
- Telegram-уведомления на каждом этапе
- Проверка доступности KAD (`https://kad.arbitr.ru`) перед деплоем

**Главный файл:** `.github/workflows/ci.yml`

**Telegram-интеграция:** `backend/app/utils/notify_telegram.py`

**Secrets:**
```

TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, PROD_SERVER_SSH_KEY,
STAGING_SERVER_SSH_KEY, PROD_SERVER_HOST, STAGING_SERVER_HOST

```

---

## 🧪 Test Guide

**Документ:** [`docs/TEST_GUIDE.md`](./TEST_GUIDE.md)

**Назначение:** Руководство по запуску и классификации тестов.

| Тип теста | Команда | Описание |
|------------|----------|-----------|
| Unit | `pytest -v` | Проверка логики и моделей |
| Smoke | `pytest -m smoke` / `make smoke` | Проверка `/api/health` |
| Integration | `pytest -m integration` / `make integration` | Проверка Telegram и KAD |
| Manual | `make telegram-notify-test` | Ручная проверка уведомлений |

**Основные Makefile-команды:**
```

make smoke
make smoke-local
make integration
make integration-local
make telegram-notify-test

```

**Файлы тестов:**
```

backend/app/tests/test_smoke_health.py
backend/app/tests/test_integration_notify.py

````

---

## 🛠️ DevOps Operations Manual

**Документ:** [`docs/DEVOPS_OPERATIONS.md`](./DEVOPS_OPERATIONS.md)

**Назначение:** Руководство по обслуживанию инфраструктуры и CI/CD.

### Основные операции:
| Команда | Назначение |
|----------|-------------|
| `make up` | Запуск контейнеров |
| `make down` | Остановка всех контейнеров |
| `make migrate` | Применение миграций Alembic |
| `make doctor` | Проверка окружения |
| `make backup-db` | Резервное копирование БД |
| `make integration` | Проверка внешних интеграций |

**Проверка контейнеров:**
```bash
docker compose -f docker-compose.prod.yml ps
docker compose -f docker-compose.prod.yml logs -f backend
````

**Бэкапы и восстановление:**

```bash
docker exec -t legal-assistant-db pg_dump -U admin legal_assistant_db > artifacts/db_backup.sql
cat artifacts/db_backup.sql | docker exec -i legal-assistant-db psql -U admin -d legal_assistant_db
```

---

## 🚀 Deploy Manual

**Документ:** [`docs/DEPLOY_MANUAL.md`](./DEPLOY_MANUAL.md)

**Назначение:** Пошаговое руководство для ручного деплоя, если CI/CD недоступен.

### Ключевые шаги

1. Подключение по SSH к серверу (`prod` или `staging`)
2. `git pull origin main`
3. `docker compose -f docker-compose.prod.yml up -d --build`
4. `make migrate`
5. `make smoke-local`
6. `make integration-local`
7. `python3 backend/app/utils/notify_telegram.py "🚀 Ручной деплой успешно завершён ✅"`

**Проверка:**

```bash
curl -s http://127.0.0.1:8080/api/health | jq
```

**Ожидаемый ответ:**

```json
{ "status": "ok" }
```

---

## 🔄 Rollback Manual

**Документ:** [`docs/ROLLBACK_MANUAL.md`](./ROLLBACK_MANUAL.md)

**Назначение:** Процедура безопасного отката версии приложения.

### Основные шаги

1. Проверка версии и бэкап:

   ```bash
   docker exec -t legal-assistant-db pg_dump -U admin legal_assistant_db > artifacts/rollback_backup.sql
   ```

2. Откат Docker-образа:

   ```bash
   docker pull ghcr.io/aw56/legal-assistant-backend:v2.3
   docker compose -f docker-compose.prod.yml up -d --force-recreate
   ```

3. Откат миграций:

   ```bash
   docker compose -f docker-compose.prod.yml exec -T backend alembic downgrade -1
   ```

4. Smoke-проверка и уведомление в Telegram:

   ```bash
   make smoke-local
   make telegram-notify-test
   ```

**Уведомление:**

> ♻️ Откат выполнен: v2.4 → v2.3 успешно завершён ✅

---

## 🧾 Deploy Log Template

**Документ:** [`docs/DEPLOY_LOG_TEMPLATE.md`](./DEPLOY_LOG_TEMPLATE.md)

**Назначение:** Шаблон журнала деплоев, rollback-ов и hotfix-ов.

### Формат записи

```
🗓️ Дата:       2025-10-09 18:45 UTC
👤 Исполнитель: GitHub Actions (CI)
🔖 Версия:      v2.4.1
🌿 Ветка:       main
⚙️ Тип:         Deploy
📊 Результат:   ✅ Успешно
Описание:       Добавлена интеграция Telegram и KAD
```

**Хранение журнала:**
`docs/DEPLOY_LOG.md` — обновляется вручную или автоматически через CI.

---

## 📘 Appendix: DevOps Principles

### Основные принципы DevOps в Legal Assistant Arbitrage

| Принцип                     | Суть                                                              |
| --------------------------- | ----------------------------------------------------------------- |
| **Automation First**        | Всё, что можно автоматизировать, должно быть в Makefile или CI    |
| **Fail Fast**               | Тесты (`--maxfail=1`) и уведомления мгновенно сообщают об ошибках |
| **Immutable Deploys**       | Каждый деплой использует новый Docker-образ с фиксированным тегом |
| **Continuous Verification** | Smoke и integration-тесты проверяют систему после каждого релиза  |
| **ChatOps Integration**     | Telegram служит главным каналом DevOps-коммуникации               |
| **Transparency**            | Все действия логируются в `docs/DEPLOY_LOG.md` и GitHub Actions   |

---

## ✅ Резюме

**Legal Assistant Arbitrage v2.4 — полностью автоматизированная DevOps-инфраструктура**, включающая:

- CI/CD пайплайн с тестами и уведомлениями
- Документированные ручные и аварийные процессы
- Telegram-интеграцию для контроля релизов
- Полную историю деплоев и rollback-ов

---

📁 **Файлы набора документации:**

| Документ                                             | Назначение                  |
| ---------------------------------------------------- | --------------------------- |
| [`CI_PIPELINE.md`](./CI_PIPELINE.md)                 | Полное описание CI/CD       |
| [`TEST_GUIDE.md`](./TEST_GUIDE.md)                   | Руководство по тестированию |
| [`DEVOPS_OPERATIONS.md`](./DEVOPS_OPERATIONS.md)     | Операции и обслуживание     |
| [`DEPLOY_MANUAL.md`](./DEPLOY_MANUAL.md)             | Ручной деплой               |
| [`ROLLBACK_MANUAL.md`](./ROLLBACK_MANUAL.md)         | Откат версии                |
| [`DEPLOY_LOG_TEMPLATE.md`](./DEPLOY_LOG_TEMPLATE.md) | Шаблон журнала релизов      |

---

🛡️ **Ответственные:**

- **DevOps Lead:** `admin@legal-assistant`
- **CI/CD Maintainer:** `ci-bot@github`
- **Infrastructure Owner:** `alex@legal-assistant.tech`

---

✍️ _Последнее обновление:_ `2025-10-09`
📦 _Версия документации:_ `v2.4.1`

```

---

📘 Теперь у тебя **полный профессиональный DevOps Handbook**,
объединяющий все технические документы проекта.

Хочешь, чтобы я помог сделать из этих Markdown-файлов единый PDF-гайд с титульной страницей,
оглавлением и стилем корпоративного руководства (`Legal Assistant Arbitrage DevOps Guide v2.4`)?
```
