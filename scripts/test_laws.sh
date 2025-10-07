#!/usr/bin/env bash
set -euo pipefail

# === Конфигурация ===
BASE_URL="http://127.0.0.1:8080/api"
TOKEN="${1:-${TOKEN:-}}"

if [ -z "$TOKEN" ]; then
  echo "❌ Ошибка: не передан токен. Использование:"
  echo "   ./scripts/test_laws.sh <ACCESS_TOKEN>"
  echo "или заранее экспортировать: export TOKEN=xxx"
  exit 1
fi

echo "✅ Используем токен: ${TOKEN:0:20}..."

# === 1. Создание закона ===
echo "➡️ Создаём закон..."
CREATE_RESP=$(curl -s -X POST "$BASE_URL/laws/" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "code": "ГПК РФ",
    "article": "ст.'"$RANDOM"'",
    "title": "Тестовый закон CRUD",
    "description": "Создан через скрипт"
  }')

echo "$CREATE_RESP" | jq
LAW_ID=$(echo "$CREATE_RESP" | jq -r '.id')

if [ "$LAW_ID" = "null" ]; then
  echo "❌ Ошибка: не удалось создать закон"
  exit 1
fi

# === 2. Чтение списка законов ===
echo "➡️ Читаем список законов..."
curl -s -X GET "$BASE_URL/laws/" \
  -H "Authorization: Bearer $TOKEN" | jq

# === 3. Обновление закона ===
echo "➡️ Обновляем закон (id=$LAW_ID)..."
curl -s -X PUT "$BASE_URL/laws/$LAW_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Обновлено скриптом"}' | jq

# === 4. Удаление закона ===
echo "➡️ Удаляем закон (id=$LAW_ID)..."
curl -s -X DELETE "$BASE_URL/laws/$LAW_ID" \
  -H "Authorization: Bearer $TOKEN" | jq

echo "✅ CRUD-тест для законов завершён успешно!"
