# 🛣️ Roadmap — Legal Assistant Arbitrage v2.5

**Версия:** v2.5 (Development)
**Период:** 2025-10-12 → 2025-10-26
**Цель:** интеграция внешних правовых источников, расширение CI/CD и стабилизация production-сборки.

---

## ✅ Предыдущая версия (v2.4 Summary)

| Компонент           | Статус | Комментарий                                    |
| ------------------- | :----: | ---------------------------------------------- |
| CI/CD AutoAuth v3.3 |   ✅   | Полный цикл прошёл успешно                     |
| Enum migrations     |   ✅   | Исправлено автоматически (`create_type=False`) |
| Regex fixer         |   ✅   | Приведён к PEP 8 и типизирован                 |
| Postman generator   |   ✅   | Минималистичный и устойчивый                   |
| Telegram ChatOps    |   ✅   | Работает стабильно                             |
| Release tag         |   ✅   | `v2.4.0` создан и запушен                      |

---

## 🎯 Цели версии v2.5

| №   | Категория         | Цель                           | Описание                                                             |
| --- | ----------------- | ------------------------------ | -------------------------------------------------------------------- |
| 1   | 🔌 Integrations   | **KAD API**                    | Подключить `kad.arbitr.ru` через `kad_service.py`                    |
| 2   | ⚖️ Integrations   | **pravo.gov.ru / data.gov.ru** | Импортировать законы и нормативные акты                              |
| 3   | 📰 Legal Data Hub | **Расширение источников**      | Добавить RG, Судебный вестник, Консультант+, Гарант                  |
| 4   | 🧠 Core           | **Backend refactor**           | Унификация импортов и абстрактный слой интеграций                    |
| 5   | 🧩 CI/CD          | **CI v3.4 pipeline**           | Добавить `docs-validate`, `format-docs`, `build-prod`, `deploy-prod` |
| 6   | 🧾 Docs           | **Автогенерация документации** | MarkdownLint + pandoc `.md → .pdf`                                   |
| 7   | 💬 ChatOps        | **Telegram v2.0**              | Уведомления о тестах, релизах и интеграциях                          |
| 8   | 🧪 Tests          | **Unit + Integration**         | Тесты для всех API-источников                                        |
| 9   | 📦 Deployment     | **Prod-ready Docker**          | Multi-stage build + healthcheck                                      |

---

## ⚙️ Этапы реализации (Stages)

### **Stage 1 — Infrastructure**

**Цель:** подготовка окружения и Makefile
**Статус:** ✅ завершено

**Выполнено:**

- Добавлены цели snapshot/patch-management в Makefile
- Создано `scripts/make_snapshot_patches.sh`
- Подключены `markdownlint` и `prettier` к pre-commit
- Проверен `Dockerfile` и `docker-compose.prod.yml` (healthcheck ОК)
- Подготовлен DevOps-гайд v2.4 (`docs/DEVOPS_PRACTICE_GUIDE.md`)

---

### **Stage 2 — Legal Data Expansion**

**Цель:** создать Legal Data Hub и агрегировать правовые источники
**Статус:** ✅ выполнено (основная логика + Redis кэш)

| Источник          | Тип                | Доступ      | Статус       |
| ----------------- | ------------------ | ----------- | ------------ |
| KAD               | Судебные дела      | ✅ REST     | Работает     |
| pravo.gov.ru      | Официальные акты   | ✅ API      | В агрегаторе |
| data.gov.ru       | Открытые данные    | ✅ REST/CSV | Планируется  |
| Российская газета | Публикации законов | ✅ RSS      | Подключается |
| Судебный вестник  | Судебная практика  | ✅ HTML     | Подключается |
| Консультант+      | Коммерческий       | ⚠️          | Заглушка     |
| Гарант            | Коммерческий       | ⚠️          | Заглушка     |

**Выполнено:**

- Создан `LegalAggregatorService` (асинхронный с Redis)
- Подключён к маршруту `/api/laws/search`
- Тест Postman (`newman_laws_search.html`) успешен

---

### **Stage 3 — CI/CD Upgrade**

**Цель:** обновление AutoAuth v3.4
**Статус:** 🟡 частично реализовано

**Выполнено:**

- Telegram-уведомления в CI (`notify_telegram.py`)
- Добавлен аудит патчей и снапшотов в Makefile

**В плане:**

- Добавить `make docs-validate` и `make format-docs`
- Проверить `build-prod` и `deploy-prod` в workflow

---

### **Stage 4 — Testing**

**Цель:** тестирование интеграций
**Статус:** 🟡 в работе

**План:**

- Unit-тесты для `KadService`, `PravoService`, `RGIntegration`, `SudVestnikIntegration`
- Моки и фикстуры API-ответов
- Интеграция pytest + Newman

---

### **Stage 5 — Release**

**Цель:** стабильный релиз v2.5
**Статус:** 🔜 ожидается (20–26 октября 2025)

**Действия:**

- Пройти AutoAuth CI v3.4 без ошибок
- Создать `artifacts/PROGRESS_YYYYMMDD.md`
- Тег `v2.5.0 → GitHub`
- Обновить README и создать `ROADMAP_v2.6.md (draft)`

---

## 📊 Метрики контроля

| Метрика          | Цель       | Текущее | Комментарий             |
| ---------------- | ---------- | ------- | ----------------------- |
| Покрытие тестами | ≥ 90 %     | ~60 %   | Юнит-тесты в разработке |
| Время CI         | ≤ 2 мин    | 1.1 мин | В норме                 |
| Markdown lint    | 100 %      | 95 %    | После `format-docs`     |
| Telegram notify  | 100 %      | 100 %   | Работает                |
| Docker image     | prod-ready | 🟡      | Проверка healthcheck    |

---

## 🔁 Автообновления и снапшоты

Каждый CI-запуск:

- создаёт `artifacts/PROGRESS_YYYYMMDD_HHMM.md`;
- делает автокоммит 📘 progress snapshot;
- пушит в GitHub с меткой `v2.5-dev`.

---

## 📎 Примечания

- API-токены → `.apitest_token` (не коммитятся)
- Интеграции через `backend/app/services/*`
- Telegram-уведомления через `notify_telegram.py`
- Документы валидируются через `markdownlint-cli2` и `prettier`

---
