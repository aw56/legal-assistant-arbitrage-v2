## 📘 3️⃣ `README_QA_ShortGuide.md`

(расширенный гайд с пояснениями и примерами)

````markdown
# Legal Assistant Arbitrage v2 — QA Documentation (Full Guide)

## 🎯 Назначение

Эта коллекция предназначена для **функционального и интеграционного тестирования** API Legal Assistant Arbitrage v2 через Postman.
Она проверяет авторизацию, работу CRUD-операций и целостность связей между сущностями.

---

## ⚙️ Как использовать

1. Импортируй:
   - `Legal Assistant Arbitrage v2.postman_collection.json`
   - `Legal Assistant Env.postman_environment.json`
2. Укажи `base_url` (например: `http://82.165.144.150:8080`)
3. Запусти **Run Collection**

---

## 🔐 AUTH

Регистрация и логин пользователя:

```json
POST /api/auth/register
{
  "username": "apitester",
  "email": "apitester@example.com",
  "password": "Test123!",
  "full_name": "API Tester"
}
```
````

После логина токен сохраняется в `{{token}}`.

---

## ⚖ LAWS

CRUD-операции для законов:

- **POST /api/laws/** → создаёт новый закон
- **GET /api/laws/** → возвращает список
- **PUT /api/laws/{{law_id}}** → обновляет
- **DELETE /api/laws/{{law_id}}** → удаляет и проверяет 404 при повторном GET

Пример:

```json
{
  "title": "Закон о тестировании API",
  "code": "2025-ТЕСТ",
  "article": "Статья 1. Тестирование API."
}
```

---

## ⚖ DECISIONS

Связаны с законами (`law_id`):

```json
POST /api/decisions/
{
  "title": "Решение суда №1",
  "summary": "Описание",
  "law_id": {{law_id}}
}
```

---

## 👥 USERS

Только авторизованный пользователь может:

- GET `/api/users/`
- PUT `/api/users/{{user_id}}`
- DELETE `/api/users/{{user_id}}`

---

## 🩺 HEALTH

`GET /api/health` → `{"status": "ok"}`

---

## 🧩 Схема зависимостей

```
User → Laws → Decisions
      ↘ Auth (JWT)
```

---

## ✅ Коды ответов

| Действие      | Код       |
| ------------- | --------- |
| Создание      | 200 / 201 |
| Обновление    | 200       |
| Удаление      | 204       |
| Ошибка токена | 401       |
| Не найдено    | 404       |
| Ошибка данных | 422       |

---

## 🧠 Советы

- Все переменные (token, law_id и др.) сохраняются автоматически.
- Коллекцию можно запускать целиком в Runner.
- После полного цикла API будет полностью протестировано.

```

```
