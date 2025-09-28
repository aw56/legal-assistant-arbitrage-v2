Отлично 🚀
Вот что мы делаем:

1. Создаём файл `docs/LOCAL_DEV.md` с подготовленным содержимым.
2. Добавляем его в git.
3. Делаем коммит.

Полный набор команд:

```bash
# Создать файл с документацией
nano docs/LOCAL_DEV.md
```

Вставь туда это содержимое:

````markdown
# 🛠 Локальная разработка (LOCAL_DEV.md)

## 📦 Подготовка окружения

### Установка зависимостей

```bash
sudo apt update
sudo apt install -y python3.12-venv python3-pip git make
````

(опционально: Docker и Compose)

```bash
sudo apt install -y docker.io docker-compose-plugin
sudo usermod -aG docker $USER
newgrp docker
```

---

## 🔐 Настройка окружения

Скопируй `.env.example` → `.env`:

```bash
cp .env.example .env
```

Для локальной разработки мы используем **SQLite**, поэтому добавь в `.env`:

```dotenv
USE_SQLITE=1
```

---

## ▶️ Запуск приложения

Локальный сервер:

```bash
make run
```

API будет доступно:

* Swagger UI → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* Healthcheck → [http://127.0.0.1:8000/api/health](http://127.0.0.1:8000/api/health)

---

## 🧪 Тестирование

Все тесты используют SQLite:

```bash
make test
```

Если хочешь переключиться на PostgreSQL (docker/prod), в `.env` поставь:

```dotenv
USE_SQLITE=0
```

---

## 🗄️ Работа с БД

### SQLite (по умолчанию)

Файл базы создаётся локально → `test.db`

Проверить таблицы:

```bash
sqlite3 test.db ".tables"
```

### PostgreSQL (docker/prod)

1. Поднять контейнеры:

```bash
make docker
```

2. Применить миграции:

```bash
alembic upgrade head
```

---

## 🧨 Troubleshooting

### Ошибка: порт 8000 занят

```bash
lsof -i :8000
kill -9 <PID>
```

### SQLite база не обновляется

Просто удали `test.db` и перезапусти сервер:

```bash
rm test.db
make run
```

---

📌 Теперь разработка локально и через тесты работает одинаково — быстро и без лишних зависимостей.

````

После сохранения файла делаем:

```bash
git add docs/LOCAL_DEV.md
git commit -m "docs: добавлена инструкция по локальной разработке (LOCAL_DEV.md)"
git push
````

Хочешь, я сразу ещё обновлю `README.md`, чтобы там была ссылка на `docs/LOCAL_DEV.md`?
