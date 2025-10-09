# 📘 DEVOPS_PRACTICE_GUIDE.md
**Legal Assistant Arbitrage v2 — Корпоративное DevOps-руководство**

---

## 1. 🎯 Введение

### Что такое DevOps
**DevOps (Development + Operations)** — это культура и набор практик, объединяющих разработку, тестирование и эксплуатацию.
Главная цель: **ускорить поставку продукта без потери качества и стабильности**.

> 🧩 DevOps — это не только инструменты, а единая система взаимодействия людей, процессов и технологий.

### Почему это важно
- Сокращает время между изменением и релизом (Lead Time)
- Повышает надёжность и повторяемость сборок
- Упрощает масштабирование инфраструктуры
- Создаёт прозрачность и совместную ответственность

---

## 2. ⚙️ Основные принципы DevOps

| Принцип | Описание |
|----------|-----------|
| **Automation** | Автоматизируй всё: сборку, тесты, деплой, уведомления |
| **Collaboration** | Разработка, тестирование и эксплуатация работают как единая команда |
| **Continuous Everything** | CI/CD — непрерывная интеграция и доставка |
| **Infrastructure as Code (IaC)** | Инфраструктура управляется кодом (Ansible/Terraform) |
| **Monitoring & Feedback** | Метрики и логи — часть системы, а не опция |
| **Security by Design (DevSecOps)** | Безопасность встраивается с самого начала |

---

## 3. 🧩 Архитектура командного DevOps-конвейера

### Общая схема

CODE → BUILD → TEST → REVIEW → DEPLOY → MONITOR → FEEDBACK → LOOP

| Этап | Цель | Инструменты |
|------|------|-------------|
| **Code** | Версионирование и контроль изменений | Git, GitHub |
| **Build** | Сборка и создание образов | Docker, Makefile |
| **Test** | Проверка логики и API | pytest, Postman/Newman |
| **CI/CD** | Автоматический пайплайн | GitHub Actions |
| **Deploy** | Развёртывание через Docker Compose | docker-compose.prod.yml |
| **Monitor** | Метрики и логи | Prometheus, Grafana |
| **Feedback** | Telegram / Slack уведомления | notify_bot, Webhooks |

---

## 4. 🧠 Культура и взаимодействие в команде

1. **Общая ответственность.**
   Dev, QA и Ops несут ответственность за стабильность релиза.

2. **Малые итерации.**
   Каждое изменение — отдельный PR.
   Релизы — минимум раз в неделю.

3. **Feature Flags.**
   Новая функциональность активируется через флаги (без риска для продакшена).

4. **Прозрачность.**
   Все пайплайны и конфигурации хранятся в Git.
   Любой может повторить процесс локально через `make`.

---

## 5. 🧰 Инструменты и стек проекта

| Категория | Используемый стек | Назначение |
|------------|------------------|-------------|
| **CI/CD** | GitHub Actions | Сборка, тестирование, деплой |
| **Контейнеризация** | Docker, Docker Compose | Изоляция сервисов |
| **IaC (опционально)** | Terraform / Ansible | Управление конфигурацией серверов |
| **Мониторинг** | Prometheus + Grafana | Метрики, алерты |
| **Логирование** | Loki / ELK Stack | Централизованный сбор логов |
| **Секреты** | .env + Docker secrets / Vault | Безопасное хранение токенов |
| **Уведомления** | Telegram Bot API | Инциденты, CI-оповещения |
| **Документация** | Markdown, MkDocs | Хранение знаний и стандартов |

---

## 6. 🧱 Корпоративные стандарты и чеклисты

### ✅ Git Workflow
- Основная ветка: `main`
- Для задач: `feature/<название>`
- Для фиксов: `fix/<название>`
- Обязательно: Pull Request + Code Review
- Коммиты в стиле Conventional Commits:
  `feat: добавлен эндпоинт /api/laws`

### ✅ Makefile стандарты
| Цель | Команда |
|------|----------|
| Проверка тестов | `make test` |
| Локальный запуск | `make run` |
| Деплой в прод | `make deploy-prod` |
| Telegram-уведомление | `make telegram-notify-test` |

### ✅ CI/CD стандарты
- Все пуши в `main` → автоматический тест и билд.
- Тесты обязательны (`pytest`, `newman`).
- При успехе → деплой через SSH / Docker Compose.
- Артефакты CI сохраняются в `artifacts/`.

---

## 7. 🔐 Безопасность и DevSecOps

| Этап | Меры безопасности |
|------|-------------------|
| **Code** | Линтер безопасности (bandit, pylint) |
| **Build** | Сканирование Docker-образов (Trivy) |
| **Deploy** | Хранение токенов в .env / secrets |
| **Run** | Ограниченные привилегии контейнеров |
| **Monitor** | Алерты об аномалиях (Prometheus Alertmanager) |

### 🔒 Чеклист DevSecOps
- [x] Secrets не коммитятся в Git
- [x] Логи не содержат персональных данных
- [x] CI/CD токены имеют только необходимые права
- [x] MFA активирован для GitHub и серверов
- [x] Автоматическое уведомление при инциденте

---

## 8. 🧭 Внедрение DevOps в команде

### Этапы внедрения
1. **Настроить CI/CD пайплайн**
   - Запуск тестов и сборки через GitHub Actions.
2. **Стандартизировать Makefile**
   - Унификация команд для всех разработчиков.
3. **Добавить мониторинг**
   - Prometheus + Grafana + Telegram alerts.
4. **Перевести инфраструктуру в код**
   - docker-compose.yml → Ansible / Terraform.
5. **Добавить ChatOps**
   - Интеграция Telegram уведомлений с CI.
6. **Ввести метрики и регулярные ретро**
   - Оценка DORA-метрик и постмортемы.

---

## 9. 📊 Метрики эффективности (DORA)

| Метрика | Цель | Что измеряет |
|----------|------|--------------|
| **Lead Time** | < 1 день | Время от коммита до релиза |
| **Deployment Frequency** | ≥ 1/день | Частота релизов |
| **MTTR** | < 1 час | Среднее время восстановления |
| **Change Failure Rate** | < 10% | Доля неудачных релизов |

---

## 10. 📚 Полезные ресурсы

| Тип | Ресурс |
|------|--------|
| 📗 Книга | *The DevOps Handbook* — Gene Kim |
| 📘 Книга | *The Phoenix Project* — Gene Kim |
| 🌐 Сайт | [12factor.net](https://12factor.net) |
| 🧰 Репозиторий | GitHub: `awesome-devops` |
| 🎥 Видео | Google Cloud — *DORA Metrics Explained* |

---

## 11. ⚡ Приложения

### Пример CI/CD пайплайна (GitHub Actions)
```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: pytest --maxfail=1 --disable-warnings -q

Пример Makefile для CI/CD
test:
	pytest --maxfail=1 --disable-warnings -q

run:
	docker compose up --build

deploy-prod:
	docker compose -f docker-compose.prod.yml up -d --build

telegram-notify-test:
	python backend/app/utils/notify_telegram.py --test

🏁 Заключение

DevOps — это не технология, а способ мышления.
Когда команда разделяет ответственность, автоматизирует рутину и измеряет результат —
продукт становится быстрее, стабильнее и безопаснее.

“You build it — you run it.”
— Werner Vogels, CTO Amazon
