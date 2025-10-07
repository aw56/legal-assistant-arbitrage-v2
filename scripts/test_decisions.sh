#!/usr/bin/env bash
set -euo pipefail

# === Конфигурация ===
BASE_URL="http://127.0.0.1:8080/api"
TOKEN="${1:-${TOKEN:-}}"

if [ -z "$TOKEN" ]; then
  echo "❌ Ошибка: не передан токен. Использование:"
  echo "   ./scripts/test_decisions.sh <ACCESS_TOKEN>"
  echo "или заранее экспортировать: export TOKEN=xxx"
  exit 1
fi

echo "✅ Используем токен: ${TOKEN:0:20}..."

# === 1. Создание решения ===
echo "➡️ Создаём решение..."
CREATE_RESP=$(curl -s -X POST "$BASE_URL/decisions/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "case_number": "A40-'"$RANDOM"'/2025",
    "court": "АС Санкт-Петербурга",
    "date_decided": "2025-10-03",
    "summary": "Тестовое решение CRUD",
    "law_id": 2,
    "user_id": 1
  }')

echo "$CREATE_RESP" | jq
DECISION_ID=$(echo "$CREATE_RESP" | jq -r '.id')

if [ "$DECISION_ID" = "null" ]; then
  echo "❌ Ошибка: не удалось создать решение"
  exit 1
fi

# === 2. Чтение списка решений ===
echo "➡️ Читаем список решений..."
curl -s -X GET "$BASE_URL/decisions/" \
  -H "Authorization: Bearer $TOKEN" | jq

# === 3. Обновление решения ===
echo "➡️ Обновляем решение (id=$DECISION_ID)..."
curl -s -X PUT "$BASE_URL/decisions/$DECISION_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"summary":"Обновлено скриптом"}' | jq

# === 4. Удаление решения ===
echo "➡️ Удаляем решение (id=$DECISION_ID)..."
curl -s -X DELETE "$BASE_URL/decisions/$DECISION_ID" \
  -H "Authorization: Bearer $TOKEN" | jq

echo "✅ CRUD-тест завершён успешно!"
