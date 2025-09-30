Отлично 🚀
Тогда держи полный файл **`docs/TROUBLESHOOTING.md`**, куда я собрал все типовые ошибки, которые мы уже ловили (psycopg2, Alembic, Docker, env, Makefile) + решения.

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

* Добавить скрипт ожидания (`wait-for-db.sh`), который проверяет доступность PostgreSQL перед стартом FastAPI.

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
ValueError: invalid interpolation syntax in 'postgresql+psycopg2://admin:Admin%402025%21@db:5432/legal_assistant_db'
```

**Причина:** `ConfigParser` интерпретирует `%` как спецсимвол.

**Решение:**

* В `env.py` указывать `config.set_main_option("sqlalchemy.url", SQLALCHEMY_URL)` (после экранирования пароля).
* Не прописывать пароль напрямую в `alembic.ini`.

---

### Ошибка

```
configparser.DuplicateOptionError: option 'script_location' already exists
```

**Причина:** в `alembic.ini` дублируется ключ.

**Решение:** оставить только один блок `[alembic]` → `script_location = migrations`.

---

## 🐳 Docker

### Ошибка

```
OCI runtime exec failed: exec failed: unable to start container process: exec: "curl": executable file not found in $PATH
```

**Причина:** в образе отсутствует `curl` (или `wget`).

**Решение:**
Добавить в Dockerfile:

```dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl wget netcat-openbsd
```

---

### Ошибка

```
Container restarting in loop (БД недоступна, повтор через 2 сек...)
```

**Причина:** бекенд стартует до инициализации базы.

**Решение:**

* Использовать `wait-for-db.sh` в `entrypoint.sh`.
* Проверить `.env` (`POSTGRES_HOST=db`, `POSTGRES_DB=legal_assistant_db`).

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
file: 'alembic.ini', line: 1
'y[alembic]\n'
```

**Причина:** битый `alembic.ini` (например, попали лишние символы при редактировании).

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

**Причина:** случайно в `.env` попал пароль вместо хоста.

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

**Решение:** убедиться, что после каждой цели (`target:`) команды начинаются с **TAB**, а не пробелов:

```makefile
up:
	docker compose -f docker-compose.prod.yml up -d --build
```

---

## ✅ Как использовать этот документ

1. Если появилась ошибка → ищи её текст в этом файле.
2. Если нет — добавляй новую секцию, чтобы не наступать на те же грабли.
3. Это "живая документация", её обновляем по мере развития проекта.

```

---

Хочешь, я сразу добавлю этот `docs/TROUBLESHOOTING.md` в git и перепишу ссылки в основном `README.md`, чтобы при любой ошибке можно было быстро перейти сюда?
```
