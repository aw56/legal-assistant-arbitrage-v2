🔥 Отлично, вот твой готовый **`README_Postman.md`** — он документирует коллекцию и окружение, описывает AutoAuth-механику, переменные, запуск и интеграцию с Makefile.
Файл можно сохранить рядом с коллекцией:
`~/my_projects/legal-assistant-arbitrage-v2/docs/README_Postman.md`

---

## ⚖️ Legal Assistant Arbitrage v2 — Postman Test Suite

**Версия:** v2.1 (AutoAuth Edition)
**Дата:** 2025-10-07

---

### 🧩 Назначение

Этот пакет предназначен для **автоматизированного функционального тестирования API Legal Assistant Arbitrage v2**.
Коллекция Postman полностью покрывает цепочку эндпоинтов:

```
/api/auth
/api/laws
/api/decisions
/api/users
/api/health
```

Особенность данной версии — **автоматическая авторизация (AutoAuth)**:
при запуске любого запроса, если токен отсутствует в окружении, Postman автоматически выполнит вход (`/api/auth/login`) с тестовыми учетными данными и сохранит `access_token`.

---

### ⚙️ Структура файлов

```
docs/
├── Legal_Assistant_Arbitrage_v2.postman_collection.json   # Коллекция (CRUD + AutoAuth)
├── Legal_Assistant_Env.postman_environment.json           # Переменные окружения
└── README_Postman.md                                      # Описание и инструкция
```

---

### 🌍 Переменные окружения

| Ключ          | Значение по умолчанию             | Назначение                |
| ------------- | --------------------------------- | ------------------------- |
| `base_url`    | `http://82.165.144.150:8080`      | Базовый URL API           |
| `token`       | _(генерируется AutoAuth)_         | JWT токен для авторизации |
| `user_id`     | _(создаётся при /auth/me)_        | ID пользователя           |
| `law_id`      | _(создаётся при POST /laws)_      | ID созданного закона      |
| `decision_id` | _(создаётся при POST /decisions)_ | ID судебного решения      |

---

### 🔐 Механизм AutoAuth

AutoAuth активируется при каждом запуске коллекции или отдельного запроса.

```js
// Пререквест в коллекции
if (!pm.environment.get("token")) {
  pm.sendRequest(
    {
      url: pm.environment.get("base_url") + "/api/auth/login",
      method: "POST",
      header: { "Content-Type": "application/json" },
      body: {
        mode: "raw",
        raw: JSON.stringify({
          username: "apitester2",
          password: "apitester123",
        }),
      },
    },
    function (err, res) {
      if (!err && res.code === 200) {
        pm.environment.set("token", res.json().access_token);
        console.log("✅ Token сохранён");
      } else {
        console.error("❌ Ошибка авторизации");
      }
    },
  );
}
```

💡 После успешного входа переменная `{{token}}` автоматически подставляется в каждый запрос в виде:

```
Authorization: Bearer {{token}}
```

---

### 🧪 CRUD-покрытие коллекции

| Категория     | Эндпоинт                     | Описание тестов                                |
| ------------- | ---------------------------- | ---------------------------------------------- |
| **AUTH**      | `/register`, `/login`, `/me` | регистрация, авторизация, получение профиля    |
| **LAWS**      | `/api/laws`                  | создание, чтение, обновление, удаление закона  |
| **DECISIONS** | `/api/decisions`             | создание, чтение, обновление, удаление решения |
| **USERS**     | `/api/users`                 | чтение, обновление, удаление пользователей     |
| **HEALTH**    | `/api/health`                | проверка доступности API                       |

---

### 🚀 Как запустить тесты

#### Через Postman (GUI)

1. Импортируй коллекцию и окружение.
2. В верхнем правом углу выбери окружение `Legal Assistant Env`.
3. Перейди во вкладку **Runner**.
4. Выбери коллекцию → нажми **Run Collection**.
5. Все запросы выполнятся последовательно, включая AutoAuth.

#### Через Makefile (сервер)

```bash
make postman HOST_URL=http://82.165.144.150:8080
make postman-export
```

После этого появится архив:

```
artifacts/postman_collection.zip
```

Скачать можно:

```bash
scp admin@82.165.144.150:/home/admin/my_projects/legal-assistant-arbitrage-v2/artifacts/postman_collection.zip C:\Users\Aleksej\Downloads\
```

или запустить локальный HTTP-сервер:

```bash
make postman-serve
```

➡️ Коллекция будет доступна по адресу
`http://82.165.144.150:8080/postman_collection.zip`

---

### 🩺 Проверка API без Postman

Быстрый smoke-тест прямо с сервера:

```bash
make health-host
```

или из контейнера:

```bash
make health-container
```

---

### ✅ Проверка в CI/CD

Рекомендуем использовать `make ci-test` для автоматической проверки API в pipeline.
AutoAuth гарантирует, что коллекция всегда авторизуется даже при свежем деплое.

---

### ✉️ Контакт

**Автор API:** Legal Assistant Team
**Тест-автор:** ChatGPT-5 QA Suite Generator
**Версия коллекции:** 2.1 AutoAuth (2025-10-07)

---

Хочешь, я добавлю в этот README в конце блок **«🧩 Расширение Postman (добавление pre-request скриптов и мониторинга через CI)»**, чтобы можно было привязать его к GitHub Actions или Jenkins?
