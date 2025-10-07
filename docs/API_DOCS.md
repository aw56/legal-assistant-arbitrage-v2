Отлично 💼 — вот полностью переработанный, отформатированный в Markdown стиль файл **`docs/API_DOCS.md`**, готовый для прямого использования в проекте или публикации в Postman / GitHub Wiki.
Он оформлен в едином стиле с архитектурным документом, с чёткими блоками, цветовой структурой и нумерацией эндпоинтов.

---

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

### 🔸 `POST /api/auth/register`
**Описание:** Регистрация нового пользователя.

**Request Body:**
```json
{
  "username": "apitest",
  "email": "apitest@example.com",
  "password": "string"
}
````

**Responses:**

* `200`: Успешная регистрация
* `422`: Ошибка валидации (уже существует / некорректные данные)

---

### 🔸 `POST /api/auth/login`

**Описание:** Аутентификация пользователя и получение JWT токена.

**Request Body:**

```json
{
  "username": "apitest",
  "password": "string"
}
```

**Responses:**

* `200`: Возвращает токен доступа
* `401`: Неверный логин или пароль

---

### 🔸 `GET /api/auth/me`

**Описание:** Получить информацию о текущем пользователе (по токену).

**Headers:**

```
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

### 🔸 `GET /api/laws/`

**Описание:** Получить список всех законов.

**Responses:**

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

### 🔸 `POST /api/laws/`

**Описание:** Создать новый закон.

**Request Body:**

```json
{
  "code": "ГПК РФ",
  "article": "ст.133",
  "title": "Принятие и возврат иска",
  "description": "Описание статьи"
}
```

**Responses:**

* `201`: Успешно создан
* `422`: Ошибка валидации

---

### 🔸 `GET /api/laws/{law_id}`

**Описание:** Получить информацию о конкретном законе.
**Параметры:** `law_id` — ID закона.

**Responses:**

```json
{
  "id": 2,
  "code": "ГПК РФ",
  "article": "ст. 131",
  "title": "Форма искового заявления"
}
```

---

### 🔸 `PUT /api/laws/{law_id}`

**Описание:** Обновить данные существующего закона.
**Параметры:** `law_id`

**Request Body:**

```json
{
  "title": "Обновлено скриптом"
}
```

**Responses:**

* `200`: Закон успешно обновлён
* `422`: Ошибка валидации

---

### 🔸 `DELETE /api/laws/{law_id}`

**Описание:** Удалить закон.
**Параметры:** `law_id`

**Responses:**

* `204`: Закон удалён
* `404`: Закон не найден

---

## 🧾 3. Судебные решения (`/api/decisions`)

### 🔸 `GET /api/decisions/`

**Описание:** Получить список всех судебных решений.

**Responses:**

```json
[
  {
    "case_number": "А40-654321/2025",
    "court": "АС Москвы",
    "summary": "Иск удовлетворён",
    "date_decided": "2025-10-03"
  }
]
```

---

### 🔸 `POST /api/decisions/`

**Описание:** Создать новое решение.

**Request Body:**

```json
{
  "case_number": "A40-12345/2025",
  "court": "АС Санкт-Петербурга",
  "date_decided": "2025-10-03",
  "summary": "Решение тестовое",
  "law_id": 2,
  "user_id": 1
}
```

**Responses:**

* `201`: Успешно создано
* `422`: Ошибка валидации

---

### 🔸 `GET /api/decisions/{decision_id}`

**Описание:** Получить одно судебное решение.

**Responses:**

```json
{
  "case_number": "A40-111111/2025",
  "court": "АС Москвы",
  "summary": "Решение обновлено",
  "date_decided": "2025-10-03"
}
```

---

### 🔸 `PUT /api/decisions/{decision_id}`

**Описание:** Обновить краткое описание решения (`summary`).

**Request Body:**

```json
{
  "summary": "Обновлено скриптом"
}
```

**Responses:**

* `200`: Успешно обновлено
* `404`: Не найдено

---

### 🔸 `DELETE /api/decisions/{decision_id}`

**Описание:** Удалить судебное решение.
**Responses:**

* `204`: Успешно удалено
* `404`: Не найдено

---

## 👥 4. Пользователи (`/api/users`)

### 🔸 `GET /api/users/`

**Описание:** Получить список пользователей.

**Responses:**

```json
[
  {
    "id": 1,
    "username": "admin",
    "email": "admin@example.com",
    "role": "superuser"
  }
]
```

---

### 🔸 `POST /api/users/`

**Описание:** Создать нового пользователя.

**Request Body:**

```json
{
  "username": "apitest2",
  "email": "apitest2@example.com",
  "password": "123456"
}
```

---

### 🔸 `GET /api/users/{user_id}`

**Описание:** Получить информацию о пользователе.
**Параметры:** `user_id`

**Responses:**

```json
{
  "id": 2,
  "username": "apitest",
  "email": "apitest@example.com",
  "role": "user"
}
```

---

### 🔸 `PUT /api/users/{user_id}`

**Описание:** Обновить данные пользователя.
**Request Body:**

```json
{
  "email": "new_email@example.com"
}
```

---

### 🔸 `DELETE /api/users/{user_id}`

**Описание:** Удалить пользователя.
**Responses:**

* `204`: Успешно
* `404`: Не найден

---

## 🧩 5. Технические эндпоинты

### 🔸 `GET /api/health`

**Описание:** Проверка состояния API.

**Responses:**

```json
{
  "status": "ok",
  "db": "connected"
}
```

---

### 🔸 `GET /api/docs/postman`

**Описание:** Скачать актуальную Postman коллекцию через API.

**Responses:**

* `200`: Возвращает `postman_collection.json`
* `404`: Коллекция не найдена

---

## 🧱 6. Корневой маршрут `/`

**Описание:** Возвращает приветственное сообщение и базовые пути API.

**Responses:**

```json
{
  "message": "⚖️ Добро пожаловать в Legal Assistant Arbitrage API",
  "docs": "/docs",
  "health": "/api/health",
  "auth": "/api/auth"
}
```

---

## 🧭 Импорт в Postman

1. Скачай коллекцию (через `make postman` или `GET /api/docs/postman`).
2. В Postman:
   → **File → Import → File**
   → выбери `postman_collection.json` или `.zip`
   → коллекция будет автоматически добавлена.
3. Укажи **Base URL** (например `http://82.165.144.150:8080`) в **Variables** для всей коллекции.

---

## 🧾 Генерация документации

Документ формируется автоматически с помощью:

```bash
python3 scripts/generate_docs.py
```

---

> 💡 **Совет:**
> Перед генерацией всегда убедись, что контейнер `backend` запущен,
> иначе `make docs` не сможет получить актуальную OpenAPI схему.

---

**Legal Assistant Arbitrage v2**
*Автоматизация юридических процессов и тестирование API — теперь в одном решении.*

```

---

✅ Файл полностью совместим с GitHub Markdown, SwaggerHub и Postman Documentation.
Хочешь, я добавлю к нему README-раздел `"🧠 Быстрый старт API"` (с curl-примерами логина и CRUD)?
Это удобно для QA и junior-разработчиков, чтобы не открывать Swagger.
```
