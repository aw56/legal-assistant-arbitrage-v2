#!/usr/bin/env python3
"""
Автогенерация Postman коллекции для Legal Assistant Arbitrage v2
с поддержкой внешнего IP (BASE_URL).
"""

import json
import os
import sys
from pathlib import Path

import requests

# === Настройки ===
DEFAULT_BASE_URL = "http://127.0.0.1:8080"
BASE_URL = (
    os.getenv("BASE_URL") or (len(sys.argv) > 1 and sys.argv[1]) or DEFAULT_BASE_URL
)
OUTPUT_FILE = Path("docs/postman_collection.json")

print(f"➡️ Используем BASE_URL: {BASE_URL}")

# === Попытка получить OpenAPI ===
spec = None
try:
    print("➡️ Пробуем получить OpenAPI через HTTP...")
    resp = requests.get(f"{BASE_URL}/openapi.json", timeout=5)
    resp.raise_for_status()
    spec = resp.json()
except Exception as e:
    print(f"⚠️ HTTP-запрос не удался: {e}")
    try:
        print("➡️ Пробуем напрямую через FastAPI...")
        from backend.app.main import app

        spec = app.openapi()
    except Exception as e2:
        print(f"❌ Ошибка: не удалось получить OpenAPI ({e2})")
        sys.exit(1)

# === Генерация Postman коллекции ===
collection = {
    "info": {
        "name": "Legal Assistant Arbitrage v2",
        "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
    },
    "item": [],
}

for path, methods in spec.get("paths", {}).items():
    for method, details in methods.items():
        request = {
            "name": f"{method.upper()} {path}",
            "request": {
                "method": method.upper(),
                "header": [{"key": "Content-Type", "value": "application/json"}],
                "url": {
                    "raw": f"{BASE_URL}{path}",
                    "protocol": "http",
                    "host": [BASE_URL.replace("http://", "").replace("https://", "")],
                    "path": [p for p in path.strip("/").split("/") if p],
                },
            },
        }
        collection["item"].append(request)

# === Сохранение ===
OUTPUT_FILE.parent.mkdir(exist_ok=True)
OUTPUT_FILE.write_text(
    json.dumps(collection, indent=2, ensure_ascii=False), encoding="utf-8"
)

print(f"✅ Postman коллекция сохранена в {OUTPUT_FILE}")
