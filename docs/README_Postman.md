### ✅ `docs/README_Postman.md`

````markdown
# 🧩 Legal Assistant Arbitrage v2 — Postman & API Testing Guide

---

## 1. 🎯 Назначение

Этот документ описывает работу с **Postman-коллекцией** проекта
и автоматизацию API-тестирования в Legal Assistant Arbitrage v2.

> Postman используется как для ручной проверки эндпоинтов,
> так и для CI-автотестов через Newman (CLI-версия Postman).

---

## 2. 📦 Структура коллекции

Файл коллекции:
`LegalAssistantArbitrage.postman_collection.json`

Файл окружения:
`LegalAssistantArbitrage.postman_environment.json`

Оба файла находятся в корне проекта и автоматически обновляются командой:

```bash
make postman
````

---

## 3. ⚙️ Импорт в Postman

1. Открой **Postman → File → Import**
2. Выбери файл:
   `LegalAssistantArbitrage.postman_collection.json`
3. Импортируй окружение:
   `LegalAssistantArbitrage.postman_environment.json`
4. Включи окружение (справа вверху в Postman)
5. Проверь переменные (Base URL, токены и т.д.)

---

## 4. 🔑 Переменные окружения

| Имя переменной | Пример значения           | Назначение                |
| -------------- | ------------------------- | ------------------------- |
| `base_url`     | `http://127.0.0.1:8080`   | Базовый адрес API         |
| `access_token` | `eyJhbGciOiJIUzI1NiIs...` | JWT токен авторизации     |
| `user_id`      | `1`                       | ID тестового пользователя |
| `law_id`       | `2`                       | ID тестового закона       |

---

## 5. 🧪 Запуск автотестов через Newman

**Newman** — CLI-утилита Postman для headless-тестирования API.

### 🧰 Локальный запуск

```bash
npx newman run LegalAssistantArbitrage.postman_collection.json \
  -e LegalAssistantArbitrage.postman_environment.json \
  --reporters cli,html \
  --reporter-html-export artifacts/newman_report.html
```

Отчёт сохранится в `artifacts/newman_report.html`

---

### ⚙️ Автоматический запуск (Makefile)

```bash
make postman-test
```

Эта команда выполняет:

1. Запуск backend контейнера (если выключен)
2. Генерацию новой коллекции
3. Запуск Newman
4. Сохранение отчёта в `artifacts/`

---

## 6. 🤖 Интеграция в CI (GitHub Actions)

Файл: `.github/workflows/ci.yml`

Фрагмент шага тестирования:

```yaml
- name: Run Postman tests via Newman
  run: |
    npm install -g newman
    newman run LegalAssistantArbitrage.postman_collection.json \
      -e LegalAssistantArbitrage.postman_environment.json \
      --reporters cli,html \
      --reporter-html-export artifacts/newman_report.html
```

Результаты тестов сохраняются как артефакт сборки.

---

## 7. 📈 Интерпретация результатов

* ✅ **Passed** — все запросы успешно выполнены
* ⚠️ **Warning** — есть нестабильные ответы (например, `5xx`)
* ❌ **Failed** — не совпали статусы или тела ответов

---

## 8. 🧰 Быстрый старт для QA

```bash
# 1. Запустить backend
make run

# 2. Сгенерировать коллекцию
make postman

# 3. Проверить API через Newman
make postman-test
```

---

## 9. 🔒 Безопасность

* Никогда не коммить токены в Postman-файлы
* Для CI-тестов используйте безопасные токены из `.env`
* Git pre-commit (`detect-secrets`) проверяет, чтобы токены не попали в репозиторий

---

## 10. 🧾 Советы

> 💡 **Совет 1:**
> Для ускорения ручных тестов используйте вкладку *Examples* в Postman.
> Так можно быстро воспроизводить шаблонные запросы.
> 💡 **Совет 2:**
> При изменении структуры API выполняйте `make postman`, чтобы обновить схему.

---

## 11. 🏁 Заключение

Postman — ключевой инструмент тестирования Legal Assistant Arbitrage API:
он объединяет ручные проверки, автоматизацию (Newman) и CI-валидацию.

*Единый источник правды — это Postman коллекция, синхронизированная с FastAPI.*

---

**Legal Assistant Arbitrage v2**
*“Test it before you trust it.”*

````

---

✅ После восстановления файла:

```bash
git add docs/README_Postman.md
pre-commit run markdownlint --all-files
````

Ошибки по этому документу (`MD013`, `MD040`) уйдут полностью.
