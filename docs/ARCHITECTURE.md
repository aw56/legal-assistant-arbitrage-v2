Отлично 💪
Вот полностью отформатированный и готовый к использованию Markdown-файл `docs/ARCHITECTURE.md`
(совмещён с разделом **Postman Integration** и оформлен в едином стиле):

---

````markdown
# ⚖️ Legal Assistant Arbitrage v2 — Архитектура и интеграция API

---

## 🏗 Общая архитектура проекта

Проект **Legal Assistant Arbitrage v2** — это модульное FastAPI-приложение, построенное на принципах чистой архитектуры и предназначенное для автоматизации юрид\
ических задач в арбитражных делах.

---

## 📂 Структура проекта

```bash
backend/
├── alembic/              # миграции Alembic
│   └── versions/
├── app/
│   ├── core/             # конфиги, безопасность, enums
│   ├── routes/           # API роуты (auth, users, laws, decisions, health, docs)
│   ├── schemas/          # Pydantic-схемы
│   ├── services/         # бизнес-логика (CRUD)
│   ├── tests/            # pytest-тесты
│   ├── database.py       # подключение к PostgreSQL
│   ├── main.py           # точка входа FastAPI
│   └── models.py         # ORM-модели (User, Law, Decision)
├── migrations/           # автогенерируемые миграции
├── seeds/                # SQL-скрипты инициализации
├── scripts/              # bash/python утилиты (тесты, docs, генерация Postman)
└── docs/                 # документация (ARCHITECTURE.md, API_DOCS.md, Postman)
```
````

---

## 🔗 Взаимодействие модулей

1. **FastAPI routes** → принимают HTTP-запросы и валидируют данные через **schemas**.
2. **services** → реализуют бизнес-логику (CRUD-операции, фильтрация, транзакции).
3. **models** → взаимодействуют с базой данных через SQLAlchemy ORM.
4. **core/security** → отвечает за аутентификацию (JWT, hashing, OAuth2).
5. **alembic** → управляет миграциями базы данных.

---

## ✅ Принципы модульности

Проект следует принципам **Clean Architecture**:

| Слой       | Назначение                     |
| ---------- | ------------------------------ |
| `routes`   | Интерфейс взаимодействия (API) |
| `services` | Основная бизнес-логика         |
| `models`   | Слой данных (ORM)              |
| `schemas`  | Валидация и сериализация       |
| `core`     | Конфигурация и утилиты         |

---

## 🧩 Интеграция с Postman

### ⚙️ Генерация Postman коллекции

Коллекция генерируется автоматически из **OpenAPI схемы FastAPI**:

```bash
make postman
```

После выполнения создаются файлы:

```
docs/postman_collection.json
artifacts/postman_collection.zip
```

---

### 📥 Способы скачивания коллекции

#### 1. Через SCP (WSL)

```bash
make postman-download HOST=admin@82.165.144.150
```

> Файл будет сохранён в
> `C:\Users\alexe\Downloads\postman_collection.zip`

---

#### 2. Через PSCP (Windows PowerShell)

```powershell
make postman-download-win HOST=admin@82.165.144.150
```

> Требуется установленный `pscp.exe` (из комплекта PuTTY).

---

#### 3. Через HTTP (браузер)

```bash
make postman-serve
```

После запуска Make покажет ссылку:

```
🌐 http://82.165.144.150:8080/postman_collection.zip
```

После скачивания нажмите **Enter**, чтобы автоматически остановить сервер.

---

### 🌍 Альтернатива — загрузка через API

Коллекцию можно скачать напрямую через endpoint:

```bash
GET /api/docs/postman
```

**Пример:**

```bash
curl -O http://82.165.144.150:8080/api/docs/postman
```

---

### 🔗 Импорт коллекции в Postman

1. Открой **Postman**
2. Перейди в **File → Import**
3. Выбери один из способов:
   - **File → выбери `postman_collection.zip`**
   - **Link → вставь ссылку**

     ```
     http://82.165.144.150:8080/api/docs/postman
     ```

---

## 🧱 Полезные команды Makefile (Postman)

| Команда                     | Описание                                |
| --------------------------- | --------------------------------------- |
| `make postman`              | Сгенерировать Postman коллекцию         |
| `make postman-download`     | Скачать коллекцию через SCP (WSL)       |
| `make postman-download-win` | Скачать через PSCP (Windows PowerShell) |
| `make postman-serve`        | Временный HTTP-сервер для скачивания    |

---

## ⚙️ Раздел Makefile (Postman)

```make
# ================================
# 📦 Postman — экспорт, загрузка и HTTP-доступ
# ================================

# 🏗 Сгенерировать Postman коллекцию и упаковать её
postman: ## 🧩 Сгенерировать Postman коллекцию
 $(MAKE) postman-export

postman-export: ## 📦 Генерация и архивирование Postman коллекции
 docker compose -f $(COMPOSE_FILE) exec backend sh -c "PYTHONPATH=/code python3 scripts/generate_postman.py"
 @mkdir -p artifacts
 zip -j artifacts/postman_collection.zip docs/postman_collection.json
 @echo "✅ Архив сохранён: artifacts/postman_collection.zip"

# 🌍 Скачать коллекцию с сервера (через SSH/SCP или HTTP)
postman-download: ## 📥 Скачать Postman коллекцию на локальный компьютер (WSL)
 @if [ -z "$(HOST)" ]; then echo "❌ Укажи сервер, пример: make postman-download HOST=admin@82.165.144.150"; exit 1; fi
 scp $(HOST):/home/admin/my_projects/legal-assistant-arbitrage-v2/artifacts/postman_collection.zip /mnt/c/Users/alexe/Downloads/
 @echo "✅ Коллекция скопирована в C:\\Users\\alexe\\Downloads\\postman_collection.zip"

postman-download-win: ## 📥 Скачать Postman коллекцию на локальный компьютер (Windows PowerShell)
 @if [ -z "$(HOST)" ]; then echo "❌ Укажи сервер, пример: make postman-download-win HOST=admin@82.165.144.150"; exit 1; fi
 pscp.exe $(HOST):/home/admin/my_projects/legal-assistant-arbitrage-v2/artifacts/postman_collection.zip C:\\Users\\alexe\\Downloads\\
 @echo "✅ Коллекция скопирована в C:\\Users\\alexe\\Downloads\\postman_collection.zip"

# 🌐 HTTP-доступ (через FastAPI) — скачивание через браузер
postman-serve: ## 🌐 Разрешить скачивание коллекции через HTTP (порт 8080)
 @echo "🚀 Запускаем временный HTTP-сервер для скачивания..."
 @cd artifacts && python3 -m http.server 8080 --bind 0.0.0.0 &
 @sleep 2
 @SERVER_PID=$$(pgrep -f "http.server 8080" | head -n1); \
 IP=$$(hostname -I | awk '{print $$1}'); \
 echo "✅ Коллекция доступна по адресу:"; \
 echo "   🌐 http://$$IP:8080/postman_collection.zip"; \
 echo ""; \
 read -p 'Нажмите [Enter] после скачивания для остановки сервера...'; \
 kill $$SERVER_PID && echo "🛑 HTTP-сервер остановлен."
```

---

## 📘 Источник документации

Документация генерируется автоматически скриптами:

```bash
python3 scripts/generate_docs.py
python3 scripts/generate_architecture.py
```

Они создают:

- `docs/API_DOCS.md`
- `docs/ARCHITECTURE.md`
- `docs/postman_collection.json`

---

## 🧾 Заключение

Интеграция Postman обеспечивает:

- полное покрытие API тестами,
- экспорт коллекций для QA и CI/CD,
- простую проверку endpoints из внешней среды (Windows, WSL, Postman Cloud).

> 🔹 Все шаги автоматизированы и доступны через Makefile.
> 🔹 Проект готов для CI/CD и документирования REST API.

---

**Legal Assistant Arbitrage v2** — единая платформа для юридической автоматизации, тестирования и анализа арбитражных дел.

```

---

💡 Хочешь, я создам аналогично оформленный `docs/API_DOCS.md` в том же стиле — с подсветкой, таблицами и нумерацией эндпоинтов для Postman?
(Это сделает API-документ ещё более наглядным для QA и клиентов).
```
