#!/bin/sh
set -e

echo "⏳ Ожидание БД ${POSTGRES_DB} (user=${POSTGRES_USER}, host=${POSTGRES_HOST})..."
/code/wait-for-db.sh

echo "⚙️ Применяем миграции Alembic..."
alembic upgrade head || {
  echo "❌ Ошибка при миграции базы"
  exit 1
}

echo "🚀 Запускаем backend..."
exec uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
