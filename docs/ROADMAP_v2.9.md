# ⚖️ Legal Assistant Arbitrage v2.9 — Integration & Intelligence Phase

_(KAD + Pravo.gov.ru + Telegram Bot + CI Integrations)_

> **Дата старта:** 16.10.2025
> **Ответственный:** Aleksej (Author & Maintainer)
> **Базовая ветка:** `main`
> **Текущая версия:** `v2.9-alpha`
> **Период спринта:** 14 дней (до 30.10.2025)

---

## 📊 Strategic Dashboard

| Компонент               | Статус            | Ключевые результаты v2.8        | План на v2.9                                         |
| ----------------------- | ----------------- | ------------------------------- | ---------------------------------------------------- |
| **CI/CD AutoAuth v3.3** | ✅ Стабильно      | Green runs, Telegram notifier   | Расширить на integrations-layer                      |
| **Makefile System**     | ✅ 100+ целей     | verify-before-change, safe-push | Добавить `make integration-test` и `make kad-update` |
| **Docs System**         | ✅ Clean Standard | v2.8 Clean                      | Ввести “Legal Intelligence Standard”                 |
| **DevSecOps Hooks**     | ✅ Рабочие        | lint + detect-secrets           | Добавить stage-integration check                     |
| **Telegram Layer**      | 🧩 70% готовности | Уведомления работают            | Реализовать чат-команды `/law`, `/case`              |
| **Integrations Layer**  | 🚧 Старт          | kad_service, pravo.gov.ru stubs | Реализовать полный сервисный слой                    |

---

## 🎯 Sprint Plan (v2.9 Alpha → Beta)

| День  | Цель                                                  | Ожидаемый результат                                |
| ----- | ----------------------------------------------------- | -------------------------------------------------- |
| 1–3   | Запуск `app/integrations/kad_service.py` + unit-mock  | CI-тест `pytest -m integration` ✅                 |
| 4–6   | Создание `app/integrations/pravo_service.py`          | HTTPX client + модель синхронизации законов        |
| 7–9   | Telegram Bot `law_assistant_bot.py` (FastAPI webhook) | Ответы на команды `/law`, `/case`                  |
| 10–11 | CI расширен до integrations                           | GitHub Actions `ci_integrations.yml`               |
| 12–13 | Docs v2.9                                             | Новый стандарт `docs/API_INTEGRATIONS_STANDARD.md` |
| 14    | Release v2.9-alpha snapshot                           | `make verify → make release → make push-safe`      |

---

## ⚙️ Технические оси развития

### 1. Integration Layer

- [ ] `app/integrations/kad_service.py` — судебные дела (KAD API)
- [ ] `app/integrations/pravo_service.py` — законы (Pravo.gov.ru / data.gov.ru)
- [ ] `app/integrations/base_service.py` — единый интерфейс адаптеров
- [ ] `app/integrations/integration_logger.py` — централизованное логирование
- [ ] `tests/integrations/test_kad_service.py` — httpx mock
- [ ] `tests/integrations/test_pravo_service.py` — schema validation

### 2. CI/CD Integrations

- [ ] Создать `.github/workflows/ci_integrations.yml`
- [ ] Добавить `make integration-test`
- [ ] Расширить `pytest.ini` с меткой `integration`
- [ ] Отчёт `artifacts/integration_report.html`
- [ ] Добавить badge `![CI Integrations](https://github.com/.../actions/workflows/ci_integrations.yml/badge.svg)`

### 3. Telegram Layer

- [ ] `app/bot/law_assistant_bot.py` — FastAPI webhook
- [ ] Команды `/law`, `/case`, `/status`
- [ ] Middleware авторизации по токену
- [ ] Ответы в формате Markdown + JSON preview
- [ ] Логи: `logs/telegram_bot.log`

### 4. Docs & Standards

- [ ] `docs/API_INTEGRATIONS_STANDARD.md` — описание структур интеграций
- [ ] `docs/DEVOPS_PRACTICE_GUIDE_v2.9.md` — CI/CD обновлён
- [ ] `docs/MAKE_PATCH_AND_RELEASE_GUIDE_v2.9.md` — единый релизный цикл
- [ ] `docs/RELEASE_v2.9_CHRONIK.md` — хронология релиза
- [ ] Обновить ссылки в `README.md` и `LOCAL_DEV.md`

---

## 🧩 Progress Snapshot System

| Команда                     | Назначение                  | Артефакт                                      |
| --------------------------- | --------------------------- | --------------------------------------------- |
| `make progress-auto-push`   | Ежедневная фиксация статуса | `artifacts/PROGRESS_YYYYMMDD_HHMM.md`         |
| `make integration-progress` | Снапшот API-интеграций      | `artifacts/PROGRESS_INTEGRATIONS_YYYYMMDD.md` |
| `make release-template`     | Подготовка шаблона релиза   | `docs/RELEASE_v2.9_TEMPLATE.md`               |

---

## 🧭 Управление потоками

| Поток              | Назначение                      | Формат                     |
| ------------------ | ------------------------------- | -------------------------- |
| **Strategic Chat** | Roadmap Control v2.9            | Еженедельный статус + план |
| **Tactical Chat**  | Integrations & Intelligence Dev | Ежедневные задачи          |
| **CI Reports**     | Автоматическая отчётность       | HTML в `artifacts/`        |

---

## 📈 Метрики контроля качества

- [ ] 100% зелёный прогон `pytest -m integration`
- [ ] 0 ошибок `markdownlint`, `yamllint`
- [ ] 0 секретов `detect-secrets`
- [ ] Telegram Bot отвечает на `/law` и `/case`
- [ ] CI Integrations badge — ✅ green
- [ ] Выпуск `v2.9-alpha` через `make push-safe`

---

## 📅 Финальный релизный чеклист

| Этап | Описание                                   | Статус |
| ---- | ------------------------------------------ | ------ |
| 1️⃣   | Все тесты green                            | ☐      |
| 2️⃣   | Документация обновлена                     | ☐      |
| 3️⃣   | CI прошёл на main                          | ☐      |
| 4️⃣   | Сформирован релизный пакет                 | ☐      |
| 5️⃣   | Ветка `v2.9-alpha` создана и зафиксирована | ☐      |
| 6️⃣   | Snapshot артефактов сохранён               | ☐      |

---

**Файл подготовлен автоматически**
Legal Assistant Arbitrage — _Integration & Intelligence Phase, v2.9-alpha_
© Aleksej, 2025
