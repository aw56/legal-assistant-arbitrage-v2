### ✅ `docs/API_DOCS.md`

````markdown
# 📖 Legal Assistant Arbitrage v2 — API Documentation

Документация автоматически сгенерирована из OpenAPI схемы FastAPI
и описывает все доступные REST endpoints проекта.

---

## ⚙️ Базовая информация

- **Base URL (локальный):** `http://127.0.0.1:8080`
- **Base URL (публичный):** `http://82.165.144.150:8080`
- **Формат данных:** JSON
- **Аутентификация:** JWT Bearer Token
- **Swagger:** [`/docs`](http://82.165.144.150:8080/docs)
- **ReDoc:** [`/redoc`](http://82.165.144.150:8080/redoc)

---

## 🔐 1. Аутентификация (`/api/auth`)

### `POST /api/auth/register`

**Описание:** Регистрация нового пользователя.

**Request Body:**

```json
{
  "username": "apitest",
  "email": "apitest@example.com",
  "password": "string"
}
```
````

**Responses:**

- `200`: Успешная регистрация
- `422`: Ошибка валидации (уже существует / некорректные данные)

---

### `POST /api/auth/login`

**Описание:** Аутентификация пользователя и получение JWT токена.

**Request Body:**

```json
{
  "username": "apitest",
  "password": "string"
}
```

**Responses:**

- `200`: Возвращает токен доступа
- `401`: Неверный логин или пароль

---

### `GET /api/auth/me`

**Описание:** Получить информацию о текущем пользователе (по токену).

**Headers:**

```text
Authorization: Bearer <ACCESS_TOKEN>
```

**Responses:**

```json
{
  "username": "apitest",
  "email": "apitest@example.com",
  "role": "user",
  "id": 2
}
```

---

## ⚖️ 2. Законы (`/api/laws`)

### `GET /api/laws/`

**Описание:** Получить список всех законов.

```json
[
  {
    "id": 2,
    "code": "ГПК РФ",
    "article": "ст. 131",
    "title": "Форма искового заявления",
    "description": "..."
  }
]
```

---

### `POST /api/laws/`

**Описание:** Создать новый закон.

```json
{
  "code": "ГПК РФ",
  "article": "ст.133",
  "title": "Принятие и возврат иска",
  "description": "Описание статьи"
}
```

---

### `GET /api/laws/{law_id}`

**Описание:** Получить информацию о конкретном законе.

```json
{
  "id": 2,
  "code": "ГПК РФ",
  "article": "ст. 131",
  "title": "Форма искового заявления"
}
```

---

### `PUT /api/laws/{law_id}`

**Описание:** Обновить данные закона.

```json
{
  "title": "Обновлено скриптом"
}
```

---

### `DELETE /api/laws/{law_id}`

**Описание:** Удалить закон.

**Responses:**

- `204`: Закон удалён
- `404`: Не найден

---

## 🧾 3. Судебные решения (`/api/decisions`)

(оставляем блоки кода и тексты как у тебя — все уже валидные)

---

## 🧱 6. Корневой маршрут `/`

**Описание:** Возвращает приветственное сообщение и базовые пути API.

```json
{
  "message": "⚖️ Добро пожаловать в Legal Assistant Arbitrage API",
  "docs": "/docs",
  "health": "/api/health",
  "auth": "/api/auth"
}
```

---

## 🧾 Генерация документации

```bash
python3 scripts/generate_docs.py
```

---

> 💡 **Совет:**
> Перед генерацией убедись, что контейнер `backend` запущен.

---

**Legal Assistant Arbitrage v2**
_Автоматизация юридических процессов и тестирование API — теперь в одном решении._

````

---

### ✅ `docs/DEVOPS_PRACTICE_GUIDE.md`

```markdown
# 📘 Legal Assistant Arbitrage v2 — Корпоративное DevOps-руководство

---

## 1. 🎯 Введение

### Что такое DevOps

DevOps (Development + Operations) — культура и набор практик, объединяющих разработку, тестирование и эксплуатацию.
Главная цель — **ускорить поставку продукта без потери качества и стабильности**.

> 🧩 DevOps — это не только инструменты, а система взаимодействия людей, процессов и технологий.

---

## 2. ⚙️ Основные принципы DevOps

| Принцип | Описание |
| -------- | -------- |
| **Automation** | Автоматизируй всё: сборку, тесты, деплой |
| **Collaboration** | Разработка, тестирование и эксплуатация работают как единая команда |
| **Continuous Everything** | CI/CD — непрерывная интеграция и доставка |
| **Infrastructure as Code** | Управление инфраструктурой через код |
| **Monitoring & Feedback** | Метрики и логи — часть системы |
| **Security by Design (DevSecOps)** | Безопасность встраивается с самого начала |

---

## 3. 🧩 Архитектура DevOps-конвейера

**CODE → BUILD → TEST → REVIEW → DEPLOY → MONITOR → FEEDBACK → LOOP**

| Этап | Цель | Инструменты |
| ---- | ---- | ----------- |
| Code | Контроль версий | Git, GitHub |
| Build | Сборка образов | Docker, Makefile |
| Test | Проверка логики | pytest, Postman/Newman |
| CI/CD | Автоматизация | GitHub Actions |
| Deploy | Развёртывание | Docker Compose |
| Monitor | Метрики | Prometheus, Grafana |
| Feedback | Уведомления | Telegram Bot, Webhooks |

---

## 4. 🧠 Культура и взаимодействие

1. Общая ответственность — Dev, QA и Ops вместе отвечают за релизы.
2. Малые итерации — каждый PR автономен, релизы еженедельные.
3. Feature Flags — включают новые фичи без риска.
4. Прозрачность — всё конфигурируется через Git и Makefile.

---

## 5. 🧰 Инструменты проекта

| Категория | Стек | Назначение |
| ---------- | ---- | ---------- |
| CI/CD | GitHub Actions | Тесты и сборки |
| Контейнеризация | Docker | Изоляция сервисов |
| IaC | Terraform / Ansible | Серверная конфигурация |
| Мониторинг | Prometheus + Grafana | Метрики и алерты |
| Логирование | Loki / ELK | Централизованный сбор |
| Секреты | .env / Vault | Безопасное хранение |
| Уведомления | Telegram Bot | CI / инциденты |
| Документация | Markdown / MkDocs | Знания и стандарты |

---

## 6. 🧱 Стандарты

### Git Workflow

- Ветка: `main`
- Задачи: `feature/<name>`
- Фиксы: `fix/<name>`
- PR + Code Review
- Коммиты в стиле Conventional Commits.

### Makefile

```makefile
test:
  pytest --maxfail=1 --disable-warnings -q

run:
  docker compose up --build

deploy-prod:
  docker compose -f docker-compose.prod.yml up -d --build

telegram-notify-test:
  python backend/app/utils/notify_telegram.py --test
````

---

## 7. 🔐 DevSecOps

| Этап    | Мера                    |
| ------- | ----------------------- |
| Code    | Bandit, pylint          |
| Build   | Trivy                   |
| Deploy  | Secrets в .env          |
| Run     | Ограничения контейнеров |
| Monitor | Alertmanager            |

---

## 8. 🧭 Внедрение

1. Настроить CI/CD.
2. Стандартизировать Makefile.
3. Добавить мониторинг.
4. Ввести IaC.
5. Настроить ChatOps.
6. Отслеживать DORA-метрики.

---

## 9. 📊 DORA-метрики

| Метрика              | Цель     | Описание             |
| -------------------- | -------- | -------------------- |
| Lead Time            | < 1 день | От коммита до релиза |
| Deployment Frequency | ≥ 1/день | Частота релизов      |
| MTTR                 | < 1 час  | Время восстановления |
| Change Failure Rate  | < 10%    | Ошибки релизов       |

---

## 10. 📚 Ресурсы

| Тип      | Ресурс                               |
| -------- | ------------------------------------ |
| 📗 Книга | _The DevOps Handbook_ — Gene Kim     |
| 📘 Книга | _The Phoenix Project_ — Gene Kim     |
| 🌐 Сайт  | [12factor.net](https://12factor.net) |
| 🧰 Repo  | `awesome-devops`                     |
| 🎥 Видео | Google Cloud — DORA Metrics          |

---

## 11. ⚡ Пример CI/CD (GitHub Actions)

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: pytest --maxfail=1 --disable-warnings -q
```

---

## 🏁 Заключение

> DevOps — это способ мышления.
> Когда команда разделяет ответственность и автоматизирует рутину — продукт становится стабильнее.

_“You build it — you run it.”_ — **Werner Vogels**, CTO Amazon

```

---
```
