Отлично 💼
Ниже — готовый и структурированный документ **`docs/CI_PIPELINE.md`**,
который описывает всю твою CI/CD-инфраструктуру проекта
**Legal Assistant Arbitrage v2.4**, включая интеграцию с Telegram, smoke и внешние проверки (KAD).

---

````markdown
# ⚖️ CI/CD Pipeline — Legal Assistant Arbitrage v2.4

## 📘 Назначение

Пайплайн CI/CD реализует **полный цикл проверки и деплоя** проекта `Legal Assistant Arbitrage`,  
включая автоматическое тестирование, сборку Docker-образов, smoke- и интеграционные тесты,  
а также Telegram-уведомления обо всех этапах.

---

## 🧩 Структура пайплайна

| Этап                  | Описание                                                          | Telegram уведомление                  |
| --------------------- | ----------------------------------------------------------------- | ------------------------------------- |
| **1. lint-and-test**  | Проверка кода (pre-commit, миграции Alembic, unit-тесты)          | ✅ успех / ❌ ошибка                  |
| **2. smoke**          | Проверка API `/api/health` и базового функционирования контейнера | ✅ API отвечает / 🚨 ошибка           |
| **3. integration**    | Проверка внешних интеграций (Telegram, KAD)                       | 🧩 успех / 🚨 сбой внешнего сервиса   |
| **4. build-and-push** | Сборка и публикация Docker-образа в GHCR                          | 📦 образ собран и опубликован         |
| **5. deploy**         | Автоматический деплой на staging или production-сервер            | 🚀 успешный деплой / ❌ ошибка деплоя |

---

## ⚙️ Основные инструменты

- **CI/CD:** GitHub Actions
- **Контейнеризация:** Docker + Docker Compose
- **Инфраструктура:** PostgreSQL, Alembic
- **Язык:** Python 3.12
- **Тесты:** Pytest (unit, smoke, integration)
- **Уведомления:** Telegram через `backend/app/utils/notify_telegram.py`

---

## 🧠 Логика пайплайна

```text
push / pull_request
       │
       ▼
┌────────────────────┐
│  lint-and-test     │
│ (pre-commit, pytest)│
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│  smoke             │
│ (docker up, /health)│
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│  integration       │
│ (Telegram, KAD)    │
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│ build-and-push     │
│ (Docker + GHCR)    │
└────────┬───────────┘
         │
         ▼
┌────────────────────┐
│ deploy             │
│ (SSH + Alembic)    │
└────────────────────┘
```
````

---

## 🔔 Telegram-интеграция

Все уведомления отправляются через модуль
`backend/app/utils/notify_telegram.py`,
использующий Markdown и переменные окружения:

```bash
TELEGRAM_BOT_TOKEN=<токен_бота>
TELEGRAM_CHAT_ID=<id_чата>
```

### Примеры сообщений

| Этап                   | Сообщение                                                               |
| ---------------------- | ----------------------------------------------------------------------- |
| ✅ CI успешно завершён | `✅ CI успешно завершён для Legal Assistant Arbitrage v2.4`             |
| 🚨 Ошибка тестов       | `❌ Ошибка CI Legal Assistant Arbitrage v2.4 — проверь логи`            |
| 🌐 Smoke OK            | `🌐 Smoke-тесты успешно пройдены: API отвечает на /health ✅`           |
| 🚨 Smoke Fail          | `🚨 Ошибка smoke-тестов: API не отвечает на /health ❌`                 |
| 🧩 Integration OK      | `🧩 Интеграционные тесты успешно завершены: Telegram и KAD доступны ✅` |
| 🚨 Integration Fail    | `🚨 Интеграционные тесты не пройдены — Telegram или KAD недоступны ❌`  |
| 📦 Image pushed        | `📦 Docker-образ успешно собран и опубликован: main`                    |
| 🚀 Deploy OK           | `🚀 Успешный деплой Legal Assistant Arbitrage v2.4 на *main*`           |

---

## 🧪 Типы тестов

| Тип теста       | Запуск                                       | Описание                             |
| --------------- | -------------------------------------------- | ------------------------------------ |
| **Unit**        | `pytest -v`                                  | базовые проверки бизнес-логики       |
| **Smoke**       | `pytest -m smoke` / `make smoke`             | проверка здоровья API и контейнера   |
| **Integration** | `pytest -m integration` / `make integration` | тест Telegram и внешнего KAD         |
| **Manual**      | `make telegram-notify-test`                  | ручная проверка Telegram-уведомлений |

---

## 🌐 Проверка внешних сервисов

### Telegram

Тест выполняет реальную отправку сообщения:

```python
send_telegram_message("🧩 Integration Test: Telegram connection OK ✅")
```

### KAD (kad.arbitr.ru)

В CI выполняется HTTP-запрос:

```python
response = httpx.get("https://kad.arbitr.ru")
assert response.status_code == 200
```

Если сайт недоступен — деплой блокируется и приходит 🚨 уведомление в Telegram.

---

## 🔐 Secrets в GitHub

В разделе
**Settings → Secrets and variables → Actions**
должны быть заданы:

| Secret                   | Назначение                    |
| ------------------------ | ----------------------------- |
| `TELEGRAM_BOT_TOKEN`     | токен Telegram-бота           |
| `TELEGRAM_CHAT_ID`       | ID получателя уведомлений     |
| `PROD_SERVER_HOST`       | адрес продакшн-сервера        |
| `PROD_SERVER_USER`       | SSH-пользователь              |
| `PROD_SERVER_SSH_KEY`    | приватный SSH-ключ для деплоя |
| `STAGING_SERVER_HOST`    | адрес staging-сервера         |
| `STAGING_SERVER_USER`    | SSH-пользователь staging      |
| `STAGING_SERVER_SSH_KEY` | SSH-ключ staging              |

---

## 🩺 Диагностика и Smoke вручную

Для локальной проверки:

```bash
make smoke-local
make integration-local
```

Для CI-диагностики:

```bash
make smoke-ci
make integration
```

---

## 📊 Отчётность и стабильность

- Все тесты и уведомления логируются в GitHub Actions и Telegram.
- Smoke и Integration имеют ограничение `--maxfail=1` и сокращённый traceback (`--tb=short`).
- В случае отказа внешних API деплой автоматически останавливается.

---

## 🧾 Источник правды

📁 Основной файл пайплайна:

```
.github/workflows/ci.yml
```

📁 Скрипт уведомлений:

```
backend/app/utils/notify_telegram.py
```

📁 Документация:

```
docs/CI_PIPELINE.md
```

---

✅ **CI/CD полностью автоматизирован.**
Пайплайн сам проверяет, собирает, тестирует и уведомляет разработчиков в Telegram
о любом изменении или сбое.

```

---

Хочешь, чтобы я сразу сгенерировал тебе и **второй документ `docs/TEST_GUIDE.md`** —
короткий гайд для разработчиков, как локально запускать все виды тестов (unit, smoke, integration, CI-эмуляция)?
```
