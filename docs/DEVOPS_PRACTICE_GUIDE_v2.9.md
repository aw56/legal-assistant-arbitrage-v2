---
# 🧩 DevOps Maintenance Commands — v2.9.7

## 📘 Назначение

Набор команд Makefile для автоисправления, форматирования и проверки всех аспектов проекта **Legal Assistant Arbitrage**.
Включён в стандарт *Full Archive Mode + Collaboration Standard v2.9.7*.
---

## ⚙️ Основные цели фиксации

| Цель                     | Назначение                                                | Инструменты                       | Статус    |
| ------------------------ | --------------------------------------------------------- | --------------------------------- | --------- |
| `make fix-docs-lint`     | Исправляет ошибки Markdown и YAML                         | `markdownlint-cli2`, `yamllint`   | ✅ Stable |
| `make fix-all-docs`      | Глубокая чистка и автоформат всех docs/                   | `prettier`, `markdownlint`, `sed` | ✅ Stable |
| `make fix-collaboration` | Проверка и автоисправление Collaboration Standard         | `markdownlint`, `yamllint`        | ✅ Stable |
| `make fix-pipeline`      | Ремонт и переинициализация pre-commit / flake8 / yamllint | `pre-commit`, `flake8`, `black`   | ✅ Stable |

---

## 🧠 Пример использования

```bash
# Автофикс всех ошибок документации
make fix-docs-lint

# Полная чистка документации и markdown
make fix-all-docs

# Проверка и выравнивание Collaboration Standard
make fix-collaboration

# Восстановление pre-commit и Python линтеров
make fix-pipeline
```
