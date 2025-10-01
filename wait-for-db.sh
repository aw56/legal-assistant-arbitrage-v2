#!/bin/sh
set -e

echo "⏳ Ожидание БД ${POSTGRES_DB} (user=${POSTGRES_USER}, host=${POSTGRES_HOST}:${POSTGRES_PORT})..."

until nc -z "${POSTGRES_HOST}" "${POSTGRES_PORT}"; do
  echo "⏳ Жду Postgres..."
  sleep 2
done

echo "✅ БД доступна"
echo "📌 DATABASE_URL=${DATABASE_URL}"

exec "$@"
