#!/usr/bin/env bash
set -euo pipefail

BASE_URL="http://127.0.0.1:8080/api"

echo "➡️ Регистрируем тестового пользователя..."
curl -s -X POST "$BASE_URL/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username":"apitest","email":"apitest@example.com","password":"secret123"}' \
  | jq

echo "➡️ Логинимся..."
TOKEN=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username":"apitest","password":"secret123"}' | jq -r .access_token)

if [[ -z "$TOKEN" || "$TOKEN" == "null" ]]; then
  echo "❌ Ошибка: не удалось получить токен"
  exit 1
fi

echo "✅ Токен получен: ${TOKEN:0:20}..."
echo "$TOKEN" > .apitest_token

echo "➡️ Проверяем /auth/me..."
curl -s -H "Authorization: Bearer $TOKEN" "$BASE_URL/auth/me" | jq
