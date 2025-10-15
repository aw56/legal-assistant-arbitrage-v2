# ⚖️ Legal Assistant Arbitrage — Roadmap v2.4

**Статус:** активная разработка
**Цель версии:** v2.3 → v2.4 (интеграции + автодокументация + CI уведомления)
**Дата обновления:** 2025-10-10

---

## 1) Видение v2.4

Стабильный backend (FastAPI + Postgres) с автоматическими интеграционными тестами (pytest + Postman), автодокументацией и ежедневной фиксацией прогресса, плюс п\
одключение внешних правовых источников (KAD, pravo.gov.ru, data.gov.ru) и уведомления в Telegram.

---

## 2) Текущее состояние (коротко)

- ✅ CI/CD: pytest + Postman v3.3 (AutoAuth) + progress snapshot + GitHub push
- ✅ SED Toolkit v3.7: безопасные массовые замены с бэкапами и CSV-логом
- ✅ Progress Toolkit v2.4: `progress-template/append/snapshot/auto-push`
- ✅ Docs генерация: `make apidocs` и `make archdocs`
- ✅ Интеграция KAD: модуль и тесты готовы
- 🧩 pravo.gov.ru / data.gov.ru: заготовки, требуется подключение
- 🚧 Telegram bot: подключение к CI уведомлениям

---

## 3) Ключевые направления работ

### A. Интеграции источников

- **KAD**: поддержка стабильна (покрыта тестами)
- **pravo.gov.ru (MVP)**:
  - Получение и разбор XML/JSON (акты/изменения)
  - Нормализация в БД (идемпотентный upsert)
  - Инкрементальные загрузки по дате
- **data.gov.ru (дополнительно)**:
  - Подключение одного релевантного набора (справочники/реестры)
  - Кэширование и таймауты

### B. Автодокументация и прогресс

- **DocsSync**: единая команда `make docs-sync` (генерация API_DOCS + ARCHITECTURE + progress-снапшот + push)
- Расширение `PROGRESS_TACTICAL.md` автозаписями из CI

### C. Уведомления и аудит CI

- **Telegram Bot**: нотификации об успешных/падающих прогонах (`test-ci-v33`, `test-ci-v3`)
- **AutoAudit JSON**: запись результатов CI в `logs/audit.json`

---

## 4) План по срокам (ориентировочно)

- **11–13 окт** — pravo.gov.ru MVP (парсер, нормализация, job)
- **13–15 окт** — Telegram CI уведомления (бот, токен, простые сообщения)
- **16–18 окт** — DocsSync (`make docs-sync`) + AutoAudit JSON
- **19–22 окт** — Вычитка/финализация документации (API + ARCHITECTURE + CI Docs)
- **23 окт** — Тег `v2.4.0-beta` + freeze багов
- **26 окт** — Релиз `v2.4`

---

## 5) Критерии готовности (DoD)

- ✅ `test-ci-v33` проходит стабильно (9/9 запросов, 0 ошибок)
- ✅ `make docs-sync` формирует и коммитит свежие `API_DOCS.md`, `ARCHITECTURE.md`, снапшот прогресса
- ✅ Telegram-уведомление об окончании CI приходит с краткой сводкой (время, статус, ссылки на отчёт)
- ✅ `pravo.gov.ru` MVP: загрузка актов, нормализация, идемпотентность, простая админ-метрика (count by date)

---

## 6) Метрики и контроль

- **CI health**: последний ран `test-ci-v33` (дата/время), длительность, assert=0 ошибок
- **Docs freshness**: время генерации `API_DOCS.md` и `ARCHITECTURE.md`
- **Ingestion**: количество новых записей из pravo.gov.ru за сутки
- **Telegram**: доставлены/не доставлены уведомления CI

---

## 7) Риски и смягчение

- **Нестабильные внешние API** → таймауты, ретраи, кеш, деградация в read-only режим
- **Разнородность данных** → схемы нормализации, валидация, идемпотентные upsert
- **Человеческий фактор** → `docs-sync` и `progress-auto-push` как ежедневный ритуал

---

## 8) Следующие задачи (по шагам)

1. Добавить `make docs-sync` и `make ci-notify` в Makefile
2. Подготовить `ingestors/pravo_gov.py` (MVP) + команду `make ingest-pravo`
3. Добавить `logs/audit.json` и запись итогов CI (`test-ci-v3`)
4. Настроить `TELEGRAM_BOT_TOKEN` и `TELEGRAM_CHAT_ID`, отсылать лаконичные итоги CI

---

## 9) Команды (удобный блок)

- Ежедневный прогресс:
  - `make progress-template` → `make progress-append` → `make progress-auto-push`
- Полный CI:
  - `make test-ci-v3` (pytest + Postman + снапшот + push)
- Автодокументация:
  - `make docs-sync` (после добавления цели)

---

## 10) Ссылки

- `docs/PROGRESS_TACTICAL.md` — тактический журнал
- `artifacts/PROGRESS_*.md` — снапшоты
- `docs/API_DOCS.md`, `docs/ARCHITECTURE.md` — автогенерация
