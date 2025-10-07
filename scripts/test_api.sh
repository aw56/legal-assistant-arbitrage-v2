#!/usr/bin/env bash
set -euo pipefail

echo "=== 🚀 Запуск интеграционных API-тестов ==="

# 1. Авторизация
./scripts/test_auth.sh

# Забираем токен
TOKEN=$(cat .apitest_token)

# 2. CRUD Законов
./scripts/test_laws.sh "$TOKEN"

# 3. CRUD Решений
./scripts/test_decisions.sh "$TOKEN"

# 4. Проверка updated_at
./scripts/test_updated_at.sh "$TOKEN"

echo "✅ Все интеграционные тесты API прошли успешно!"
