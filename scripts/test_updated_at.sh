#!/usr/bin/env bash
set -euo pipefail

TOKEN=${1:-${TOKEN:-}}

if [ -z "$TOKEN" ]; then
  echo "❌ Ошибка: не передан токен. Использование:"
  echo "   ./scripts/test_updated_at.sh <ACCESS_TOKEN>"
  echo "или заранее экспортировать: export TOKEN=xxx"
  exit 1
fi

echo "✅ Используем токен: ${TOKEN:0:20}..."

# Создаём уникальный case_number для теста
CASE_NUM="A40-UPDATED-$(date +%s)"

echo "➡️ Создаём новое решение..."
CREATE_RESP=$(curl -s -X POST http://127.0.0.1:8080/api/decisions/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"case_number\":\"$CASE_NUM\",
    \"court\":\"АС Тестовый\",
    \"date_decided\":\"2025-10-03\",
    \"summary\":\"Тестируем updated_at\",
    \"law_id\":2,
    \"user_id\":1
  }")

echo "$CREATE_RESP" | jq

ID=$(echo "$CREATE_RESP" | jq -r .id)
CREATED_AT=$(echo "$CREATE_RESP" | jq -r .created_at)
UPDATED_AT=$(echo "$CREATE_RESP" | jq -r .updated_at)

echo "📌 ID=$ID | created_at=$CREATED_AT | updated_at=$UPDATED_AT"

# Приведём к timestamp (секунды)
CREATED_TS=$(date -d "$CREATED_AT" +%s)
UPDATED_TS=$(date -d "$UPDATED_AT" +%s)

# Проверка согласованности времён
if [ "$UPDATED_TS" -lt "$CREATED_TS" ]; then
  echo "❌ Ошибка: updated_at меньше created_at"
  exit 1
elif [ $((UPDATED_TS - CREATED_TS)) -le 1 ]; then
  echo "✅ updated_at корректно инициализировано (≈ created_at)"
else
  echo "⚠️ Предупреждение: разница между created_at и updated_at больше 1 секунды"
fi

echo "➡️ Обновляем summary..."
UPDATE_RESP=$(curl -s -X PUT http://127.0.0.1:8080/api/decisions/$ID \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"summary":"Тестовое обновление"}')

NEW_UPDATED_AT=$(echo "$UPDATE_RESP" | jq -r .updated_at)
echo "📌 После обновления: updated_at=$NEW_UPDATED_AT"

if [ "$NEW_UPDATED_AT" != "$UPDATED_AT" ]; then
  echo "✅ updated_at обновилось корректно"
else
  echo "❌ Ошибка: updated_at не изменилось при апдейте"
  exit 1
fi
