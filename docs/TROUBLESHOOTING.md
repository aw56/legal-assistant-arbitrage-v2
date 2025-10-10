# 📄 `docs/TROUBLESHOOTING.md`

```markdown
# 🛠 TROUBLESHOOTING — Legal Assistant Arbitrage v2

Этот документ содержит **каталог типовых ошибок и решений**, которые уже встречались при разработке и деплое проекта.

---

## 🐘 PostgreSQL / psycopg2

### Ошибка
```

psycopg2.OperationalError: could not translate host name "2025!@db" to address: Name or service not known

````

**Причина:** в строке подключения не был экранирован пароль, содержащий `@` или `!`.

**Решение:**
- Использовать `urllib.parse.quote_plus` для безопасного экранирования пароля:

```python
from urllib.parse import quote_plus
DB_PASS = quote_plus(os.getenv("POSTGRES_PASSWORD", ""))
````

---

### Ошибка

```
psycopg2.OperationalError: connection refused
```

**Причина:** контейнер `backend` стартует быстрее, чем `db`.

**Решение:**

- Использовать `wait-for-db.sh` перед запуском FastAPI.
- Если данные повреждены — выполнить:

```bash
make reset-db
```

---

## 📜 Alembic

### Ошибка

```
FAILED: No 'script_location' key found in configuration.
```

**Причина:** в `alembic.ini` отсутствует секция `[alembic]`.

**Решение:**

```ini
[alembic]
script_location = migrations
sqlalchemy.url =
```

---

### Ошибка

```
ValueError: invalid interpolation syntax ...
```

**Причина:** пароль с `%` интерпретируется как спецсимвол.

**Решение:** использовать `config.set_main_option("sqlalchemy.url", SQLALCHEMY_URL)` в `migrations/env.py`.

---

### Ошибка

```
configparser.DuplicateOptionError: option 'script_location' already exists
```

**Причина:** в `alembic.ini` дублируется ключ.

**Решение:** оставить только один блок `[alembic]`.

---

## 🐳 Docker

### Ошибка

```
OCI runtime exec failed: exec failed: "curl": executable file not found
```

**Причина:** в образе отсутствует `curl` (или `wget`).

**Решение:** добавить в Dockerfile:

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends curl wget netcat-openbsd
```

---

### Ошибка

```
Container restarting in loop (БД недоступна, повтор через 2 сек...)
```

**Причина:** backend стартует до инициализации базы.

**Решение:**

- Использовать `wait-for-db.sh`.
- Проверить `.env`.
- Если нужно пересоздать БД:

```bash
make reset-db
```

---

### Ошибка

```
WARN[0000] the attribute `version` is obsolete, it will be ignored
```

**Причина:** в `docker-compose.yml` или `docker-compose.prod.yml` указано `version:`.

**Решение:** удалить строку `version: "3.9"` — в новых версиях Docker Compose она не нужна.

---

## 🔐 .env и конфиги

### Ошибка

```
configparser.MissingSectionHeaderError: File contains no section headers.
```

**Причина:** битый `alembic.ini`.

**Решение:** переписать `alembic.ini` начисто:

```ini
[alembic]
script_location = migrations
sqlalchemy.url =
```

---

### Ошибка

```
POSTGRES_HOST=2025!@db
```

**Причина:** пароль случайно попал вместо хоста.

**Решение:** исправить `.env`:

```dotenv
POSTGRES_USER=admin
POSTGRES_PASSWORD=Admin@2025!
POSTGRES_DB=legal_assistant_db
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

---

## 📄 Makefile

### Ошибка

```
Makefile:5: *** missing separator.  Stop.
```

**Причина:** вместо табуляции в рецепте использованы пробелы.

**Решение:** убедиться, что после каждой цели команды начинаются с **TAB**, а не пробелов.

---

## ✅ Как использовать этот документ

1. Если появилась ошибка → ищи её текст в этом файле.
2. Если нет — добавляй новую секцию.
3. Для полной очистки окружения и пересоздания БД всегда есть:

```bash
make reset-db
```

```

---

Хочешь, я сразу подготовлю для тебя коммит: добавим эти два файла и перепишем ссылки на них в основном `README.md`?
```
