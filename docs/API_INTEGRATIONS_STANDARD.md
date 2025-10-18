---

# 🧩 API Integrations Standard — v2.9
### Legal Assistant Arbitrage Integration Layer v2.9

> **Версия:** 1.0 (v2.9-alpha)
> **Дата:** 16.10.2025
> **Автор:** Aleksej (Maintainer)
> **Применимо к:** `app/integrations/*`
> **Цель:** стандартизировать подключение и тестирование внешних источников (KAD, Pravo.gov.ru, Telegram Bot)

---

## 📚 1. Общие принципы

1. Все интеграции реализуются в виде изолированных сервисов внутри папки `app/integrations/`.
2. Каждый сервис наследует базовый интерфейс `BaseIntegrationService`, реализующий:
   - стандартные методы `fetch()`, `parse()`, `store()`;
   - внутренний метод `_request()` с httpx-обёрткой;
   - унифицированное логирование через `integration_logger.py`.
3. Все вызовы внешних API выполняются **асинхронно** (`httpx.AsyncClient`).
4. Исключения обрабатываются через кастомный класс `IntegrationError`.
5. Для всех интеграций обязательно наличие:
   - модульных тестов (`tests/integrations/test_<service>.py`);
   - моков запросов (`respx` / `pytest-mock`);
   - описания схем в этом стандарте.

---

## ⚖️ 2. KAD Integration (kad.arbitr.ru)

**Назначение:** получение и обновление данных арбитражных дел.

**Модуль:** `app/integrations/kad_service.py`

### 2.1 Конфигурация

| Параметр       | Тип  | Описание                                                    |
| -------------- | ---- | ----------------------------------------------------------- |
| `KAD_BASE_URL` | str  | Базовый URL API (например, `https://kad.arbitr.ru/KadAPI/`) |
| `KAD_TIMEOUT`  | int  | Таймаут запроса, сек                                        |
| `KAD_HEADERS`  | dict | Заголовки с User-Agent и Accept                             |

### 2.2 Методы API

| Метод                    | Endpoint                         | Описание                                |
| ------------------------ | -------------------------------- | --------------------------------------- |
| `fetch_case_by_number()` | `/api/case?number={case_number}` | Получить дело по номеру                 |
| `fetch_cases_by_inn()`   | `/api/cases?inn={inn}`           | Получить список дел по ИНН              |
| `parse_case()`           | —                                | Разбор и нормализация ответа            |
| `store_case()`           | —                                | Сохранение данных в таблицу `decisions` |

### 2.3 Пример схемы ответа (упрощённо)

```json
{
  "case_number": "А40-12345/2025",
  "court_name": "АС г. Москвы",
  "plaintiff": "ООО «Ромашка»",
  "defendant": "ПАО «Сигма»",
  "decision_date": "2025-09-15",
  "result": "Иск удовлетворён частично"
}

---

## 📂 Placement Appendix

**Текущее расположение Integration Layer (v2.9):**

**Архитектурная эволюция (v3.0):**

🧭 Данное размещение утверждено в рамках фазы **Integration & Intelligence (v2.9)**
и документировано в файле `docs/INTEGRATIONS_BASE_SERVICE_GUIDE.md`.

📘 *Фиксировано архитектором Aleksej — 16.10.2025*
```
