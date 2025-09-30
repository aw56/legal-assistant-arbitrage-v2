#!/bin/sh
set -e

host="${POSTGRES_HOST:-db}"
port="${POSTGRES_PORT:-5432}"
db="${POSTGRES_DB:-postgres}"

echo "⏳ Ожидание БД ${db} (user=${POSTGRES_USER}, host=${host}:${port})..."
until nc -z "$host" "$port"; do
  echo "БД недоступна, повтор через 2 сек..."
  sleep 2
done
echo "✅ БД доступна"
