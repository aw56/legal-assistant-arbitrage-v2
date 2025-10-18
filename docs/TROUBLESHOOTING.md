---
title: "TROUBLESHOOTING — Legal Assistant Arbitrage v2.9"
version: "2.9.7"
author: "Aleksej — Project Owner"
created: "2025-10-13"
status: "✅ Stable"
description: "Справочник по диагностике и устранению частых проблем Legal Assistant Arbitrage API"
---

# ⚙️ TROUBLESHOOTING — Legal Assistant Arbitrage v2.9

## 📋 Оглавление

1. [PostgreSQL / psycopg2](#1-postgresql--psycopg2)
2. [Alembic](#2-alembic)
3. [Docker](#3-docker)
4. [.env и конфиги](#4-env-и-конфиги)
5. [Makefile](#5-makefile)
6. [CI/CD и зависимости](#6-cicd-и-зависимости)
7. [Общие команды восстановления](#7-общие-команды-восстановления)
8. [Как пользоваться документом](#8-как-пользоваться-документом)

---

## 🐘 1. PostgreSQL / psycopg2

### ⚠️ Проблема

Ошибка подключения к базе данных:

```

sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server failed

```

### 💡 Решение

1. Проверь, запущен ли контейнер:

   ```bash
   docker ps | grep legal-assistant-db
   ```

````

2. Если не запущен — подними сервис:

   ```bash
   make docker-up
   ```

3. Проверь строку подключения в `.env`:

   ```dotenv
   DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/legal_assistant
   ```

---

## ⚙️ 2. Alembic

### ⚠️ Проблема

Миграции не применяются:

```
sqlalchemy.exc.NoReferencedTableError: Foreign key associated with column could not find table
```

### 💡 Решение

1. Убедись, что таблицы созданы:

   ```bash
   make db-init
   ```

2. Прогоняй миграции в правильной среде:

   ```bash
   make alembic-upgrade
   ```

3. Если конфликт версий — очисти и пересоздай:

   ```bash
   alembic downgrade base && alembic upgrade head
   ```

---

## 🐳 3. Docker

### ⚠️ Проблема

Контейнер падает при запуске с ошибкой `exit code 1`.

### 💡 Решение

1. Пересобери образы:

   ```bash
   make docker-rebuild
   ```

2. Удали старые контейнеры:

   ```bash
   docker-compose down -v
   ```

3. Проверь порты:

   ```bash
   lsof -i :8000
   ```

4. Если занят — освободи:

   ```bash
   kill -9 <PID>
   ```

---

## ⚙️ 4. .env и конфиги

### ⚠️ Проблема

`.env` не подхватывается или переменные пусты.

### 💡 Решение

1. Проверь корректность формата:

   ```bash
   cat .env | grep DATABASE_URL
   ```

2. Убедись, что `.env` в корне проекта.

3. В Docker добавь:

   ```yaml
   env_file:
     - .env
   ```

4. Для локальных тестов:

   ```bash
   export $(grep -v '^#' .env | xargs)
   ```

---

## 🧱 5. Makefile

### ⚠️ Проблема

Ошибка при выполнении команд:

```
make: *** No rule to make target 'lint'.  Stop.
```

### 💡 Решение

1. Проверь версию Make:

   ```bash
   make --version
   ```

2. Убедись, что ты в корне проекта (`~/my_projects/legal-assistant-arbitrage-v2`).

3. Обнови `Makefile` через pull:

   ```bash
   git pull origin main
   ```

4. Выполни проверку целей:

   ```bash
   make help
   ```

---

## 🚨 6. CI/CD и зависимости

### ⚠️ Проблема

CI падает с ошибкой flake8 или pre-commit.

### 💡 Решение

1. Запусти локально:

   ```bash
   pre-commit run --all-files
   ```

2. Если есть ошибки автоисправления:

   ```bash
   pre-commit clean && pre-commit install
   ```

3. Проверь токены GitHub Actions в настройках репозитория (раздел `Secrets → Actions`).

---

## 🩺 7. Общие команды восстановления

### 🔧 Сброс виртуального окружения

```bash
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 🔧 Очистка кешей и временных файлов

```bash
rm -rf __pycache__ .pytest_cache logs artifacts tmp
```

### 🔧 Полная переинициализация проекта

```bash
make reset-all
```

---

## 📚 8. Как пользоваться документом

Этот документ предназначен для **быстрого устранения ошибок** при разработке и тестировании Legal Assistant Arbitrage API.

Каждая секция содержит:

* типовую проблему;
* шаги диагностики;
* команды для исправления;
* контрольные проверки после выполнения.

Перед каждым релизом рекомендуется запускать:

```bash
make fix-docs-lint
```

чтобы сохранять консистентность Markdown-файлов и корректность ссылок.

---

✅ **Совместимость:** `markdownlint-cli2 v0.18.1`
✅ **Стиль:** `General Clean Standard v2.9`
📅 Последняя ревизия: 2025-10-16
👤 Ответственный: **Aleksej (Project Owner)**
````
