#!/usr/bin/env python3
"""
Автогенерация ARCHITECTURE.md для Legal Assistant Arbitrage v2
"""

from pathlib import Path

ARCH_FILE = Path("docs/ARCHITECTURE.md")

CONTENT = """# 🏗️ Архитектура проекта — Legal Assistant Arbitrage v2"

Документ сгенерирован автоматически скриптом `scripts/generate_architecture.py`.

---

## 📂 Структура проекта

```bash
backend/
├── alembic/              # миграции Alembic
│   └── versions/
├── app/
│   ├── core/             # конфиги, безопасность, enums
│   ├── routes/           # API роуты (auth, users, laws, decisions, health)
│   ├── schemas/          # Pydantic-схемы
│   ├── services/         # бизнес-логика (CRUD)
│   ├── tests/            # pytest-тесты
│   ├── database.py       # подключение к PostgreSQL
│   ├── main.py           # точка входа FastAPI
│   └── models.py         # ORM-модели (User, Law, Decision)
├── migrations/           # автогенерируемые миграции
├── seeds/                # SQL-скрипты инициализации
└── scripts/              # bash/python утилиты (тесты, docs)
docs/                     # документация


"""
