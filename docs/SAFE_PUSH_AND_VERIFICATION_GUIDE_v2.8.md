---
title: "Safe Push & Verification Guide"
version: "v2.8"
author: "Aleksej — Project Owner"
created: "2025-10-15"
status: "✅ Stable"
description: "Пошаговое руководство по проверке и безопасному пушу изменений в Legal Assistant Arbitrage API"
---

## 🧩 Safe Push & Verification Guide — Legal Assistant Arbitrage v2.8

### ⚙️ 1. Проверка перед изменениями

```bash
make verify-before-change
Проверяет:

окружение Python и Docker;

линтеры black, isort, flake8;

документацию markdownlint / yamllint;

pre-commit хуки.

🚀 2. Безопасный пуш
bash
Копировать код
make safe-push
Выполняет:

Полную проверку;

Автокоммит;

Пуш в ветку release/v2.8-dev.

📊 Итог проверки
bash
Копировать код
✅ Verification finished.
💾 All fixed files committed.
🚀 Push successful to release/v2.8-dev.
📅 Последняя ревизия: 2025-10-16
👤 Ответственный: Aleksej (Project Owner)
