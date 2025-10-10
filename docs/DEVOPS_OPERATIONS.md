Отлично ⚙️
Вот полноценный и детально структурированный документ
**`docs/DEVOPS_OPERATIONS.md`**, описывающий все DevOps-процессы,
обслуживание CI/CD пайплайна и действия при сбоях для проекта
**Legal Assistant Arbitrage v2.4**.

---

````markdown
# ⚙️ DEVOPS OPERATIONS — Legal Assistant Arbitrage v2.4

## 📘 Назначение

Этот документ описывает основные DevOps-процессы проекта  
**Legal Assistant Arbitrage v2.4**: управление CI/CD, контейнерами, миграциями, резервным копированием и SSH-деплоем.  
Он служит практическим руководством для разработчиков и администраторов при поддержке системы в рабочем состоянии.

---

## 🧱 1. Архитектура и окружение

| Компонент          | Назначение                   |
| ------------------ | ---------------------------- |
| **FastAPI**        | основной backend-сервис      |
| **PostgreSQL**     | база данных                  |
| **Docker Compose** | управление контейнерами      |
| **GitHub Actions** | CI/CD пайплайн               |
| **Alembic**        | миграции базы данных         |
| **Telegram Bot**   | уведомления о статусах CI/CD |
| **GHCR.io**        | реестр Docker-образов        |

---

## 🧭 2. Основной цикл деплоя

1. Разработчик делает `git push` в ветку `main` или `staging`.
2. Автоматически запускается **GitHub Actions CI/CD**:
   - ✅ lint и тесты,
   - 🚦 smoke `/api/health`,
   - 🧩 интеграции (Telegram и KAD),
   - 🐳 build & push Docker image,
   - 🚀 деплой на сервер (через SSH).
3. Результаты приходят в **Telegram-уведомлении**.

---

## 🧰 3. Команды Makefile для DevOps

| Команда             | Описание                     |
| ------------------- | ---------------------------- |
| `make up`           | Запуск контейнеров           |
| `make down`         | Остановка всех контейнеров   |
| `make restart`      | Перезапуск backend и БД      |
| `make migrate`      | Применение Alembic миграций  |
| `make wait-for-api` | Ожидание готовности API      |
| `make smoke`        | Проверка здоровья API        |
| `make integration`  | Проверка Telegram и KAD      |
| `make deploy`       | Выполнение деплоя через SSH  |
| `make doctor`       | Проверка состояния окружения |
| `make backup-db`    | Резервное копирование БД     |

---

## 🧩 4. Контроль контейнеров

### Просмотр состояния

```bash
docker compose -f docker-compose.prod.yml ps
```
````

### Логи backend

```bash
docker compose -f docker-compose.prod.yml logs -f backend
```

### Перезапуск backend без остановки БД

```bash
docker compose -f docker-compose.prod.yml restart backend
```

### Полный перезапуск всех контейнеров

```bash
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d --build
```

---

## 🗄️ 5. Миграции и база данных

### Применить миграции

```bash
make migrate
```

### Создать новую миграцию

```bash
alembic revision -m "add new field to laws"
```

### Проверить текущую версию

```bash
docker exec -it legal-assistant-backend alembic current
```

### Проверить соединение с БД

```bash
docker exec -it legal-assistant-db psql -U admin -d legal_assistant_db -c "SELECT now();"
```

---

## 💾 6. Резервное копирование базы данных

### Ручное создание бэкапа

```bash
docker exec -t legal-assistant-db pg_dump -U admin legal_assistant_db > artifacts/db_backup_$(date +'%Y%m%d_%H%M%S').sql
```

### Автоматическая загрузка в S3 (пример)

```bash
aws s3 cp artifacts/db_backup_$(date +'%Y%m%d_%H%M%S').sql s3://legal-assistant-backups/
```

### Восстановление из бэкапа

```bash
cat artifacts/db_backup_2025_10_09.sql | docker exec -i legal-assistant-db psql -U admin -d legal_assistant_db
```

---

## 🛰️ 7. SSH-деплой на сервер

### Условия

- SSH-ключ хранится в GitHub Secrets:
  `PROD_SERVER_SSH_KEY` или `STAGING_SERVER_SSH_KEY`.
- Цель деплоя определяется веткой:
  - `main` → production
  - `staging` → staging

### Проверка доступа

```bash
ssh -i ~/.ssh/prod_legal_assistant.pem user@your-server-ip
```

### Вручную перезапустить деплой

```bash
make deploy
```

---

## 🔔 8. Telegram-уведомления

### Проверить вручную

```bash
make telegram-notify-test
```

### Типы уведомлений

| Этап             | Пример                         |
| ---------------- | ------------------------------ |
| CI Success       | ✅ CI успешно завершён         |
| Smoke Fail       | 🚨 Ошибка smoke-тестов         |
| Integration Fail | 🚨 Telegram или KAD недоступны |
| Deploy OK        | 🚀 Успешный деплой             |
| Deploy Fail      | ❌ Ошибка деплоя               |

---

## 🔍 9. Диагностика и восстановление

### Проверка состояния окружения

```bash
make doctor
```

### Проверка API

```bash
curl -s http://127.0.0.1:8080/api/health | jq
```

### Проверка логов пайплайна

```bash
gh run list
gh run view <run_id>
```

### Очистка кэша Docker

```bash
docker system prune -af
```

---

## 🚨 10. Действия при сбоях

| Проблема                     | Действие                                               |
| ---------------------------- | ------------------------------------------------------ |
| CI падает на smoke           | Проверить `/api/health`, контейнеры backend/db         |
| Ошибка интеграции            | Проверить Telegram токен и kad.arbitr.ru               |
| Deploy не проходит           | Проверить SSH Secrets и логи `appleboy/ssh-action`     |
| Alembic конфликт             | Выполнить `make migrate` локально, закоммитить ревизию |
| Telegram не шлёт уведомления | Проверить `TELEGRAM_BOT_TOKEN` и `TELEGRAM_CHAT_ID`    |

---

## 🧾 11. Полный цикл обновления системы

```bash
git pull origin main
make down
docker system prune -af
make up
make migrate
make wait-for-api
make smoke-local
make integration-local
```

Если все тесты пройдены — система готова к деплою.

---

## 🧠 12. Рекомендации DevOps

- Минимизируй ручное SSH-вмешательство — CI/CD автоматизирует всё.
- Проверяй Telegram-уведомления после каждого пуша в `main`.
- Делай бэкапы БД перед крупными обновлениями Alembic.
- Не храни ключи и токены в `.env` — используй **GitHub Secrets**.
- Раз в неделю выполняй `make doctor` для технического осмотра окружения.

---

## 📜 Источники

| Файл                                   | Назначение                      |
| -------------------------------------- | ------------------------------- |
| `.github/workflows/ci.yml`             | Конфигурация CI/CD              |
| `Makefile`                             | Основные DevOps-команды         |
| `backend/app/utils/notify_telegram.py` | Telegram уведомления            |
| `docker-compose.prod.yml`              | Продакшн контейнеры             |
| `docs/CI_PIPELINE.md`                  | Документация пайплайна          |
| `docs/TEST_GUIDE.md`                   | Гайд по тестированию            |
| `docs/DEVOPS_OPERATIONS.md`            | Текущий файл (DevOps процедуры) |

---

✅ **Legal Assistant Arbitrage v2.4**
CI/CD и DevOps-инфраструктура полностью автоматизированы.
Разработчик получает обратную связь в Telegram и GitHub в течение минуты после пуша.

```

---

Хочешь, чтобы я дополнил комплект документации четвёртым файлом —
`docs/DEPLOY_MANUAL.md`, где будет описан **поэтапный ручной деплой** (если CI/CD временно отключён)?
```
