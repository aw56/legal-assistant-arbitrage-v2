---

# ⚖️ Legal Assistant Arbitrage v2.9 — Integration & Intelligence Phase

### KAD + Pravo.gov.ru + Telegram Bot + CI Integrations

## 📊 Strategic Dashboard (v2.9 Launch — 16.10.2025)

| Компонент               | Статус            | Ключевые результаты v2.8        | План на v2.9                                         |
| ----------------------- | ----------------- | ------------------------------- | ---------------------------------------------------- |
| **CI/CD AutoAuth v3.3** | ✅ Стабильно       | Green runs, Telegram notifier   | Расширить на integrations-layer                      |
| **Makefile System**     | ✅ 100+ целей      | verify-before-change, safe-push | Добавить `make integration-test` и `make kad-update` |
| **Docs System**         | ✅ Чистая база     | v2.8 Clean Standard             | Ввести “Legal Intelligence Standard”                 |
| **DevSecOps Hooks**     | ✅ Активны         | lint + detect-secrets           | Добавить stage-integration check                     |
| **Telegram Layer**      | 🧩 Готовность 70% | Уведомления работают            | Добавить чат-обработку команд `/law`, `/case`        |
| **Integrations**        | 🚧 Старт          | kad_service, pravo.gov.ru stubs | Реализовать полный сервисный слой                    |

---

## 🎯 14-дневный Sprint Plan (v2.9 Alpha → Beta)

| День  | Цель                                                  | Результат                                          |
| ----- | ----------------------------------------------------- | -------------------------------------------------- |
| 1–3   | Запуск `app/integrations/kad_service.py` + unit-mock  | CI-тест `pytest -m integration` ✅                 |
| 4–6   | Создать `app/integrations/pravo_service.py`           | HTTPX client + law sync model                      |
| 7–9   | Telegram Bot `law_assistant_bot.py` (FastAPI webhook) | Ответы на команды `/law`, `/case`                  |
| 10–11 | CI расширен до integrations                           | GitHub Actions `ci_integrations.yml`               |
| 12–13 | Docs v2.9                                             | Новый стандарт `docs/API_INTEGRATIONS_STANDARD.md` |
| 14    | Release v2.9-alpha snapshot                           | `make verify → make release → make push-safe`      |

---

## ⚙️ Технические оси развития

1. **Интеграционный слой**
   - `app/integrations/kad_service.py` — судебные дела (KAD API)
   - `app/integrations/pravo_service.py` — законы (Pravo.gov.ru / data.gov.ru)
   - Единый адаптер `BaseIntegrationService`
   - Модуль логирования `integration_logger.py`

2. **CI/CD**
   - `ci_integrations.yml` — автономный пайплайн
   - Тестирование через `pytest + respx + httpx.AsyncClient`
   - Автогенерация отчёта `artifacts/integration_report.html`

3. **Telegram Layer**
   - Вебхуки `/webhook/telegram` (FastAPI)
   - Авторизация через API-токен
   - Слоты команд `/law`, `/case`, `/status`
   - Ответ в формате Markdown + JSON preview

4. **Документация**
   - `docs/API_INTEGRATIONS_STANDARD.md` — структура всех интеграций
   - `docs/ROADMAP_v2.9.md` — живой план-таблица
   - `docs/DEVOPS_PRACTICE_GUIDE_v2.9.md` — расширение CI-практик

---

## 🧩 Progress Snapshot System

Сохраняем предыдущий стандарт фиксации:

```bash
make progress-auto-push
# → artifacts/PROGRESS_YYYYMMDD_HHMM.md
```

Дополнительно добавляем:

```bash
make integration-progress
# → artifacts/PROGRESS_INTEGRATIONS_YYYYMMDD.md
```

---

## 🧭 Контроль и поддержка

- **Стратегический чат:** `Legal Assistant Arbitrage v2.9 — Roadmap Control`
- **Тактический чат:** `Legal Assistant Arbitrage v2.9 — Integrations & Intelligence Development`
- **CI отчетность:** `artifacts/newman_report_v34.html`, `artifacts/integration_report.html`

---

Если подтверждаешь — я:

1. сгенерирую готовый файл `docs/ROADMAP_v2.9.md` с этим содержанием (в чистом Markdown-формате под твою структуру репозитория),
2. добавлю базовую секцию под CI-интеграции (KAD, Pravo, Telegram) и пустые чекбоксы для прогресса.

Создаю `docs/ROADMAP_v2.9.md` сейчас?
