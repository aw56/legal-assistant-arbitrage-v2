Отлично ✅
Сейчас мы создадим:

1. **Makefile-команду** `test-ci`, чтобы запускать Postman-тесты одной строкой.
2. **Документацию (README_CI_Postman.md)** — полное описание, как использовать CI-тесты, отчёты, и откуда берутся токены и окружение.

---

## 🧩 1. Добавь в `Makefile`

Файл: `Makefile` (корень проекта)

```makefile
# === Postman / Newman CI тестирование ===

# Генерация CI-отчёта Postman
test-ci:
	@echo "🚀 Запуск Newman CI тестов (AutoAuth, CRUD, Cleanup)..."
	newman run docs/Legal_Assistant_Arbitrage_v3_CI.postman_collection.json \
	  -e docs/Legal_Assistant_Env.postman_environment.json \
	  --reporters cli,html \
	  --reporter-html-export artifacts/newman_report.html
	@echo "✅ Отчёт создан: artifacts/newman_report.html"
```

📌 **Запуск тестов:**

```bash
make test-ci
```

🎯 **Результат:**

* Отработают все CRUD-тесты с автоавторизацией.
* В консоли появится краткий отчёт Newman.
* В `artifacts/newman_report.html` будет HTML-отчёт (готов к CI/CD публикации).

---

## 📘 2. Создай документацию:

Файл: `docs/README_CI_Postman.md`

````markdown
# 🧪 CI-Тестирование API через Postman (AutoAuth)

## 📋 Описание
Этот комплект (`Legal_Assistant_Arbitrage_v3_CI`) предназначен для **полностью автономного тестирования API** проекта *Legal Assistant Arbitrage v2*.
Он работает без ручного ввода токена — **авторизация выполняется автоматически**.

---

## 🚀 Быстрый старт

### 1️⃣ Проверка Newman и репортёров
Убедись, что установлены:
```bash
npm install -g newman newman-reporter-html
````

### 2️⃣ Запуск тестов

Используй одну команду:

```bash
make test-ci
```

Или вручную:

```bash
newman run docs/Legal_Assistant_Arbitrage_v3_CI.postman_collection.json \
  -e docs/Legal_Assistant_Env.postman_environment.json \
  --reporters cli,html \
  --reporter-html-export artifacts/newman_report.html
```

---

## ⚙️ Что делает тест

| Этап                | Описание                                                                          | Проверка |
| ------------------- | --------------------------------------------------------------------------------- | -------- |
| **Auth (AutoAuth)** | Регистрирует нового случайного пользователя, затем логинится и сохраняет `token`. | ✅        |
| **User Info**       | Проверяет доступ к `/api/auth/me`                                                 | ✅        |
| **Laws CRUD**       | Создаёт, обновляет и удаляет закон                                                | ✅        |
| **Decisions CRUD**  | Создаёт и удаляет судебное решение (привязанное к `law_id`)                       | ✅        |
| **Cleanup**         | Удаляет созданные объекты и проверяет, что база очищена                           | ✅        |
| **Health**          | Проверяет `/api/health`                                                           | ✅        |

---

## 🧰 Переменные окружения (`docs/Legal_Assistant_Env.postman_environment.json`)

| Переменная                 | Значение по умолчанию           | Назначение              |
| -------------------------- | ------------------------------- | ----------------------- |
| `base_url`                 | `http://82.165.144.150:8080`    | URL API                 |
| `token`                    | (устанавливается автоматически) | JWT-токен               |
| `user_id`                  | (устанавливается автоматически) | ID пользователя         |
| `law_id`                   | (устанавливается автоматически) | ID закона               |
| `decision_id`              | (устанавливается автоматически) | ID решения              |
| `rand_user` / `rand_email` | Генерируются перед тестом       | Уникальный пользователь |

---

## 📊 Отчёты

После выполнения тестов:

* Консоль покажет результаты по каждому запросу.
* HTML-отчёт сохраняется в:

  ```
  artifacts/newman_report.html
  ```

Можно открыть его прямо в браузере:

```
file:///home/admin/my_projects/legal-assistant-arbitrage-v2/artifacts/newman_report.html
```

---

## 🧩 Использование в CI/CD

Добавь шаг в GitHub Actions / GitLab CI:

```yaml
- name: Run API Tests
  run: make test-ci
```

💡 Результаты можно публиковать как артефакт:

```yaml
- name: Upload Newman report
  uses: actions/upload-artifact@v3
  with:
    name: newman-report
    path: artifacts/newman_report.html
```

---

## 🧠 Отладка

Если хочешь проверить окружение вручную:

```bash
newman run docs/Legal_Assistant_Arbitrage_v3_CI.postman_collection.json -d --verbose
```

Если API работает не на 8080:

```bash
export BASE_URL=http://127.0.0.1:8000
make test-ci
```

---

## ✅ Результат

После успешного прогона:

```
✔ AUTH — AutoAuth
✔ LAWS CRUD
✔ DECISIONS CRUD
✔ CLEANUP
✔ HEALTH CHECK
```

🎯 Отчёт: `artifacts/newman_report.html`

```

---

Хочешь, я сразу соберу это всё в ZIP-архив `postman_ci_package.zip` (коллекция + окружение + README + Makefile-фрагмент) для переноса на Windows или CI-сервер?
```
