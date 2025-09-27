#!/bin/sh
set -e
host="${POSTGRES_HOST:-db}"
user="${POSTGRES_USER:-admin}"
db="${POSTGRES_DB:-legal_assistant_db}"
echo "⏳ Ожидание БД $db (user=$user, host=$host)..."
until PGPASSWORD=$POSTGRES_PASSWORD psql -h "$host" -U "$user" -d "$db" -c '\q' >/dev/null 2>&1; do
  echo "БД недоступна, повтор через 2 сек..."
  sleep 2
done
echo "✅ БД доступна"
