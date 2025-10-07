#!/bin/sh
set -e

echo "🚀 Старт entrypoint.sh"
echo "🔑 Переменные окружения:"
echo "  POSTGRES_USER=${POSTGRES_USER}"
echo "  POSTGRES_DB=${POSTGRES_DB}"
echo "  POSTGRES_HOST=${POSTGRES_HOST}"
echo "  POSTGRES_PORT=${POSTGRES_PORT}"
echo "  DATABASE_URL=${DATABASE_URL}"

# Ждём БД
/code/wait-for-db.sh

# Применяем миграции
echo "⚙️ Применяем миграции Alembic..."
alembic upgrade head || { echo "❌ Ошибка миграций"; exit 1; }

# Запускаем приложение
echo "✅ Запускаем Uvicorn..."
exec uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
