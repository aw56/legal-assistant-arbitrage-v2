---
title: "Roadmap — Legal Assistant Arbitrage v2.9"
version: "v2.9-alpha"
author: "Aleksej — Project Owner"
created: "2025-10-16"
status: "✅ Active"
description: "План развития версии v2.9 (Integration & Intelligence Phase)"
---

# ⚖️ Legal Assistant Arbitrage v2.9 — Integration & Intelligence Phase

### (KAD + Pravo.gov.ru + Telegram Bot + CI Integrations)

> **Дата старта:** 2025-10-16
> **Ответственный:** Aleksej (Maintainer)
> **Период спринта:** 14 дней (до 2025-10-30)

---

## 📊 Strategic Dashboard

| Компонент           | Статус            | Результаты v2.8          | Цель v2.9                          |
| ------------------- | ----------------- | ------------------------ | ---------------------------------- |
| CI/CD AutoAuth v3.3 | ✅ Stable         | Green runs               | Расширить integrations             |
| Makefile System     | ✅ 100+ целей     | verify-before-change     | Добавить integration-test          |
| Docs System         | ✅ Clean Standard | v2.8 clean               | Ввести Legal Intelligence Standard |
| DevSecOps Hooks     | ✅ Рабочие        | lint + detect-secrets    | Добавить stage-integration         |
| Telegram Layer      | 🧩 70%            | уведомления              | команды `/law`, `/case`            |
| Integrations Layer  | 🚧 В работе       | kad_service, pravo stubs | полный слой                        |

---

## 🎯 Sprint Plan (v2.9 Alpha → Beta)

| День  | Цель                                          | Ожидаемый результат                      |
| ----- | --------------------------------------------- | ---------------------------------------- |
| 1–3   | `app/integrations/kad_service.py` + unit-mock | CI-тест ✅                               |
| 4–6   | `app/integrations/pravo_service.py`           | синхронизация законов                    |
| 7–9   | Telegram Bot webhook                          | ответы `/law`, `/case`                   |
| 10–11 | CI integrations расширен                      | GitHub Actions badge                     |
| 12–13 | Docs v2.9                                     | API Integration Standard                 |
| 14    | Release snapshot                              | `make verify → make release → push-safe` |

---

## 📈 Метрики качества

- [x] `pytest -m integration` — 100% green
- [x] markdownlint / yamllint — clean
- [x] detect-secrets — pass
- [x] Telegram Bot отвечает на `/law`, `/case`
- [x] CI integrations badge — ✅

---

📅 Последняя ревизия: 2025-10-16
👤 Ответственный: **Aleksej (Project Owner)**
