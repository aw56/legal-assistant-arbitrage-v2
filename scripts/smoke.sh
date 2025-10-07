#!/usr/bin/env bash
set -euo pipefail

API="http://127.0.0.1:8080/api"

echo "=== 🚦 Smoke Test Legal Assistant API ==="

fail() {
  echo "❌ $1"
  exit 1
}

# --- Health ---
echo "[1] Healthcheck..."
HEALTH=$(curl -s ${API}/health | jq -r .status || fail "Health endpoint broken")
[[ "$HEALTH" == "ok" ]] || fail "Health not OK"
echo "✅ Health OK"

# --- Register ---
echo "[2] Register user..."
REGISTER=$(curl -s -o /dev/null -w "%{http_code}" -X POST ${API}/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"smokeuser","password":"secret"}')

if [[ "$REGISTER" == "201" || "$REGISTER" == "400" ]]; then
  echo "✅ User registered (or already exists)"
else
  fail "Register failed (status=$REGISTER)"
fi

# --- Login ---
echo "[3] Login..."
TOKEN=$(curl -s -X POST ${API}/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=smokeuser&password=secret" | jq -r .access_token)

[[ "$TOKEN" != "null" && -n "$TOKEN" ]] || fail "Login failed"
echo "✅ Got JWT token"

# --- Me ---
echo "[4] Profile /me..."
curl -s ${API}/auth/me -H "Authorization: Bearer $TOKEN" | jq . || fail "/me failed"
echo "✅ /me works"

# --- Laws CRUD ---
echo "[5] Create law..."
LAW_ID=$(curl -s -X POST ${API}/laws/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"code":"GK","title":"ГК РФ","article":"10","description":"Злоупотребление правом"}' \
  | jq -r .id)

[[ "$LAW_ID" =~ ^[0-9]+$ ]] || fail "Law not created"
echo "✅ Law created id=$LAW_ID"

echo "[6] List laws..."
curl -s ${API}/laws/ | jq . || fail "List laws failed"

echo "[7] Delete law..."
DEL_LAW=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE ${API}/laws/${LAW_ID})
[[ "$DEL_LAW" == "200" ]] || fail "Law delete failed"
echo "✅ Law deleted"

# --- Decisions CRUD ---
echo "[8] Create decision..."
DEC_ID=$(curl -s -X POST ${API}/decisions/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"case_number":"A40-12345/2020","court":"АС Москвы","date_decided":"2020-05-20","summary":"тестовое решение","law_id":'${LAW_ID}'}' \
  | jq -r .id)

[[ "$DEC_ID" =~ ^[0-9]+$ ]] || fail "Decision not created"
echo "✅ Decision created id=$DEC_ID"

echo "[9] List decisions..."
curl -s ${API}/decisions/ | jq . || fail "List decisions failed"

echo "[10] Delete decision..."
DEL_DEC=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE ${API}/decisions/${DEC_ID})
[[ "$DEL_DEC" == "200" ]] || fail "Decision delete failed"
echo "✅ Decision deleted"

echo "=== 🎉 Smoke tests PASSED ==="
