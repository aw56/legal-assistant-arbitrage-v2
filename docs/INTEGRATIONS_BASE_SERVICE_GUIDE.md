---

# 🧩 INTEGRATIONS BASE SERVICE GUIDE — v2.9
### Legal Assistant Arbitrage Integration Layer v2.9

> **Версия:** 1.0
> **Дата:** 16.10.2025
> **Автор:** Aleksej (Maintainer)
> **Связанные файлы:**
>
> - `app/integrations/base_service.py`
> - `app/integrations/kad_service.py`
> - `app/integrations/pravo_service.py`
> - `docs/API_INTEGRATIONS_STANDARD.md`

---

## 📘 1. Назначение

`base_service.py` — это **базовый (родительский)** класс для всех внешних интеграций в Legal Assistant Arbitrage.
Он задаёт **единый интерфейс** и **общие правила работы** для всех модулей, взаимодействующих с внешними API (KAD, Pravo.gov.ru, Telegram Bot, Контур и т.д.).

---

## 🧱 2. Проблема, которую решает

Без унификации каждая интеграция дублирует однотипный код:

- подключение `httpx.AsyncClient`;
- обработка ошибок и таймаутов;
- логирование;
- парсинг и сохранение данных.

Пример “до”:

```python
# kad_service.py (без базового класса)
async def fetch_case(...):
    client = httpx.AsyncClient()
    try:
        r = await client.get(...)
        return r.json()
    except Exception:
        ...

---

## 📂 Размещение и эволюция

**Текущее размещение (v2.9):**

**Архитектурное обоснование:**
Файл находится в составе `Integration Layer` и служит общим каркасом для всех внешних API-интеграций (KAD, Pravo.gov.ru, Telegram и др.).
Это расположение обеспечивает прозрачность структуры и логическую близость ко всем наследуемым сервисам (`kad_service.py`, `pravo_service.py` и т.д.).

**Планируемая эволюция (v3.0):**

На следующем этапе развития проекта (v3.x) планируется перенос интеграционного слоя в `core/`
в составе инфраструктурного ядра приложения (вместе с `core/db`, `core/logging`, `core/scheduler`).

---

📘 *Фиксировано решением архитектора Aleksej — Integration & Intelligence Phase, 16.10.2025.*
```
