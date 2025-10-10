Отлично ✅
Вот готовый, профессионально оформленный документ
**`docs/TEST_GUIDE.md`** — полный гайд для разработчиков по локальному и CI-тестированию
в проекте **Legal Assistant Arbitrage v2.4**.

Он структурирован, подходит и для onboarding новых участников, и для внутреннего контроля качества.

---

````markdown
# 🧪 TEST GUIDE — Legal Assistant Arbitrage v2.4

## 📘 Назначение

Этот документ описывает **все типы тестов**, используемые в проекте,  
и порядок их локального и CI-запуска.  
Гайд помогает разработчикам и DevOps-инженерам быстро проверять  
качество кода, стабильность API и корректность внешних интеграций (Telegram, KAD).

---

## ⚙️ 1. Подготовка окружения

Перед запуском тестов убедись, что у тебя установлены:

- Python **3.12+**
- Docker + Docker Compose
- PostgreSQL (через Docker)
- Установлены зависимости проекта:
  ```bash
  pip install -r requirements-dev.txt
  ```
````

### Активируй виртуальное окружение

```bash
source venv/bin/activate
```

---

## 🧩 2. Основные директории

| Раздел              | Путь                                   | Назначение                          |
| ------------------- | -------------------------------------- | ----------------------------------- |
| Тесты               | `backend/app/tests/`                   | Все unit, smoke и integration тесты |
| Конфиг Pytest       | `pytest.ini`                           | Настройки, фильтры и маркеры        |
| Скрипты уведомлений | `backend/app/utils/notify_telegram.py` | Telegram-интеграция                 |
| CI/CD конфиг        | `.github/workflows/ci.yml`             | Полный пайплайн CI/CD               |

---

## 🧠 3. Типы тестов

### 3.1 Unit-тесты (модульные)

Проверяют бизнес-логику, модели и сервисные функции без обращения к сети.

**Запуск:**

```bash
pytest -v --maxfail=1 --tb=short
```

**Пример:**

```python
def test_add_law(client):
    response = client.post("/api/laws", json={"code": "CIV", "article": "1", "title": "Test Law"})
    assert response.status_code == 200
```

---

### 3.2 Smoke-тесты

Быстрая проверка “жизнеспособности” API и контейнера.
Используются как локально, так и в CI.

**Файл:** `backend/app/tests/test_smoke_health.py`

**Запуск:**

```bash
pytest -m smoke -v
```

**Через Makefile:**

```bash
make smoke
```

**Результат:**

```text
✅ API отвечает на /api/health
```

---

### 3.3 Integration-тесты

Проверяют соединение с внешними сервисами — **Telegram** и **KAD (kad.arbitr.ru)**.

**Файлы:**

- `backend/app/tests/test_integration_notify.py` — тест Telegram
- встроенный KAD-тест в `.github/workflows/ci.yml`

**Запуск локально:**

```bash
export TELEGRAM_BOT_TOKEN="твой_токен"
export TELEGRAM_CHAT_ID="твой_chat_id"
make integration-local
```

**В Telegram придёт сообщение:**

> 🧩 Integration Test: Telegram connection OK ✅

Если тест упадёт — бот отправит уведомление о сбое:

> 🚨 Интеграционные тесты упали локально — проверь Telegram или KAD ❌

---

## 🧰 4. Makefile команды тестирования

| Команда                     | Назначение                                     |
| --------------------------- | ---------------------------------------------- |
| `make test`                 | Запуск всех тестов                             |
| `make smoke`                | Smoke-тесты (в CI)                             |
| `make smoke-local`          | Smoke-тесты локально + Telegram alert          |
| `make integration`          | Интеграционные тесты в CI                      |
| `make integration-local`    | Интеграционные тесты локально + Telegram alert |
| `make telegram-notify-test` | Проверка Telegram-интеграции вручную           |

---

## 🧪 5. Тестирование CI-пайплайна локально

Для эмуляции CI можно запустить последовательность тестов вручную:

```bash
make smoke-local
make integration-local
pytest -v
```

**Полный цикл CI в GitHub Actions:**

1. Линтинг и юнит-тесты
2. Smoke `/api/health`
3. Integration (Telegram, KAD)
4. Build + Push Docker
5. Deploy на сервер

---

## 🌐 6. Проверка Telegram-интеграции вручную

1. Убедись, что бот создан через [@BotFather](https://t.me/BotFather)
2. Получи токен и chat_id
3. Выполни команду:

   ```bash
   make telegram-notify-test
   ```

4. В Telegram придёт сообщение:

   > ✅ Проверка Telegram уведомлений — Legal Assistant Arbitrage v2.4

---

## ⚖️ 7. Проверка KAD (kad.arbitr.ru)

Для проверки доступности КАД:

```bash
python3 - <<'PYCODE'
import httpx
url = "https://kad.arbitr.ru"
r = httpx.get(url, timeout=10)
print("✅ KAD доступен" if r.status_code == 200 else f"❌ KAD вернул {r.status_code}")
PYCODE
```

**Примечание:** этот тест выполняется автоматически на этапе `integration` в CI.

---

## 🩺 8. Отладка тестов

Если хочешь подробные логи при ошибках:

```bash
pytest -vv --maxfail=1 --tb=long
```

Если нужно видеть все print() внутри тестов:

```bash
pytest -s -m integration
```

---

## 🔐 9. Переменные окружения для тестов

| Переменная           | Назначение                      |
| -------------------- | ------------------------------- |
| `DATABASE_URL`       | строка подключения к PostgreSQL |
| `TELEGRAM_BOT_TOKEN` | токен Telegram-бота             |
| `TELEGRAM_CHAT_ID`   | ID Telegram-чата                |
| `ENV`                | режим (`dev`, `test`, `prod`)   |

---

## 📋 10. Рекомендации

- Используй `pytest.mark.integration` и `pytest.mark.smoke` для классификации тестов.
- Не коммить реальные токены или ключи в репозиторий.
- При ошибках Telegram или KAD тесты должны **фейлиться с понятным сообщением**.
- Всегда проверяй, что `make smoke` и `make integration` проходят **чисто** перед пушем в `main`.

---

## 🧾 Резюме

| Цель                         | Команда                     |
| ---------------------------- | --------------------------- |
| Полный тестовый цикл         | `pytest -v`                 |
| Smoke-тесты                  | `make smoke`                |
| Интеграция Telegram и KAD    | `make integration`          |
| Telegram-уведомление вручную | `make telegram-notify-test` |

---

✅ **Legal Assistant Arbitrage v2.4**
Тестовая инфраструктура полностью автоматизирована
и синхронизирована с пайплайном CI/CD.

```

---

Хочешь, чтобы я подготовил третий документ — `docs/DEVOPS_OPERATIONS.md`,
где будет описано, как обслуживать пайплайн (перезапуск CI, сброс контейнеров, SSH-деплой и резервное копирование)?
```
