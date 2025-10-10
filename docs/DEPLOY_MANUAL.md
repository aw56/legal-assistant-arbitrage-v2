Отлично 🚀
Вот завершённый и тщательно проработанный документ
**`docs/DEPLOY_MANUAL.md`** — практическое руководство по **ручному деплою проекта Legal Assistant Arbitrage v2.4**,
если CI/CD временно недоступен или требуется аварийное развертывание.

---

````markdown
# 🚀 DEPLOY MANUAL — Legal Assistant Arbitrage v2.4

## 📘 Назначение

Этот документ описывает **пошаговый ручной процесс деплоя** проекта  
**Legal Assistant Arbitrage v2.4**, включая сборку Docker-образа, миграции, перезапуск контейнеров  
и проверку доступности API.  
Используется в случае недоступности CI/CD пайплайна или при первичном развертывании на сервере.

---

## 🧩 1. Подготовка окружения

Перед началом убедись, что на сервере установлены:

| Компонент      | Проверка                                             |
| -------------- | ---------------------------------------------------- |
| Docker         | `docker --version`                                   |
| Docker Compose | `docker compose version`                             |
| Python 3.12+   | `python3 --version`                                  |
| Git            | `git --version`                                      |
| PostgreSQL     | `docker ps` → контейнер `legal-assistant-db` активен |

---

## 🔐 2. SSH-доступ к серверу

Подключись к серверу:

```bash
ssh -i ~/.ssh/prod_legal_assistant.pem user@your-server-ip
```
````

Если деплой идёт на staging:

```bash
ssh -i ~/.ssh/staging_legal_assistant.pem user@staging-server-ip
```

После входа убедись, что проект находится в `/opt/legal-assistant/`.

```bash
cd /opt/legal-assistant
```

---

## 🧱 3. Получение последней версии кода

```bash
git fetch origin main
git checkout main
git pull origin main
```

Проверь ветку:

```bash
git branch
```

Ожидается: `* main`

---

## 🐳 4. Сборка и запуск контейнеров

### Полная сборка с нуля

```bash
docker compose -f docker-compose.prod.yml down
docker system prune -af
docker compose -f docker-compose.prod.yml up -d --build
```

### Проверка состояния контейнеров

```bash
docker compose -f docker-compose.prod.yml ps
```

Ожидается, что активны:

- `legal-assistant-backend`
- `legal-assistant-db`

---

## 🗄️ 5. Применение миграций Alembic

```bash
docker compose -f docker-compose.prod.yml exec -T backend alembic upgrade head
```

Если возникает ошибка миграции:

```bash
docker compose -f docker-compose.prod.yml exec -T backend alembic current
docker compose -f docker-compose.prod.yml exec -T backend alembic history
```

---

## ❤️ 6. Проверка здоровья API

Проверь, что сервер отвечает:

```bash
curl -s http://127.0.0.1:8080/api/health | jq
```

Ожидаемый ответ:

```json
{
  "status": "ok"
}
```

Если контейнер работает на другом порту:

```bash
curl -s http://0.0.0.0:8080/api/health
```

---

## 🧠 7. Smoke-тест после деплоя

```bash
make smoke-local
```

или вручную:

```bash
pytest -m smoke -v
```

Если все тесты зелёные:

```
✅ Все smoke-тесты успешно пройдены!
```

---

## 🌐 8. Проверка интеграций (Telegram и KAD)

### Telegram

```bash
make telegram-notify-test
```

Ожидается сообщение:

> 🚀 Legal Assistant Arbitrage: тестовое уведомление от CI

### KAD ([https://kad.arbitr.ru](https://kad.arbitr.ru))

```bash
python3 - <<'PYCODE'
import httpx
r = httpx.get("https://kad.arbitr.ru", timeout=10)
print("✅ KAD доступен" if r.status_code == 200 else f"❌ KAD недоступен ({r.status_code})")
PYCODE
```

---

## 📦 9. Ручная сборка и пуш Docker-образа

Если GHCR (GitHub Container Registry) недоступен,
можно собрать и загрузить образ вручную.

```bash
docker build -t legal-assistant-backend:manual -f Dockerfile .
docker tag legal-assistant-backend:manual ghcr.io/aw56/legal-assistant-backend:manual
docker push ghcr.io/aw56/legal-assistant-backend:manual
```

---

## 🧾 10. Перезапуск backend без полной остановки

```bash
docker compose -f docker-compose.prod.yml restart backend
```

---

## 🩺 11. Диагностика при ошибках

| Симптом                 | Проверка / Решение                                           |
| ----------------------- | ------------------------------------------------------------ |
| ❌ `API not responding` | `docker logs legal-assistant-backend`                        |
| ❌ Ошибка миграции      | `docker exec -it backend alembic heads`                      |
| ❌ Telegram не шлёт     | Проверить `TELEGRAM_BOT_TOKEN` и `CHAT_ID`                   |
| ❌ Нет соединения с БД  | Проверить контейнер `legal-assistant-db` и переменные `DB_*` |
| ❌ KAD недоступен       | Проверить HTTPS и DNS, возможно кратковременный сбой         |

---

## 💾 12. Резервное копирование перед деплоем

Перед запуском деплоя рекомендуется сделать бэкап БД:

```bash
docker exec -t legal-assistant-db pg_dump -U admin legal_assistant_db > artifacts/db_backup_$(date +'%Y%m%d_%H%M%S').sql
```

---

## 🔄 13. Проверка после деплоя

1. Перейди в браузере:

   ```
   http://<SERVER_IP>:8080/docs
   ```

2. Убедись, что FastAPI UI открывается.
3. Проверь endpoints `/api/health`, `/api/laws`, `/api/decisions`.
4. Проверь Telegram: должно прийти сообщение

   > ✅ Успешный деплой Legal Assistant Arbitrage v2.4 на _main_

---

## 🧹 14. Очистка старых контейнеров и кэша

```bash
docker system prune -af
docker volume prune -f
```

---

## 🛠️ 15. Восстановление из бэкапа

```bash
cat artifacts/db_backup_2025_10_09.sql | docker exec -i legal-assistant-db psql -U admin -d legal_assistant_db
```

---

## 🔔 16. Telegram-уведомления при ручном деплое

Для ручного информирования разработчиков:

```bash
python3 backend/app/utils/notify_telegram.py "🚀 Ручной деплой Legal Assistant Arbitrage v2.4 завершён успешно ✅"
```

или при ошибке:

```bash
python3 backend/app/utils/notify_telegram.py "❌ Ошибка ручного деплоя Legal Assistant Arbitrage v2.4 — проверь сервер!"
```

---

## 📋 17. Контрольная последовательность (чеклист деплоя)

| Этап | Команда                        | Ожидание                          |
| ---- | ------------------------------ | --------------------------------- |
| 1    | `git pull origin main`         | ✅ актуальный код                 |
| 2    | `docker compose down`          | ✅ контейнеры остановлены         |
| 3    | `docker system prune -af`      | 🧹 очищен кэш                     |
| 4    | `docker compose up -d --build` | 🐳 контейнеры запущены            |
| 5    | `make migrate`                 | 🗄️ применены миграции             |
| 6    | `make smoke-local`             | 🚦 проверен API                   |
| 7    | `make integration-local`       | 🧩 проверены Telegram и KAD       |
| 8    | `make doctor`                  | 🩺 окружение в порядке            |
| 9    | Telegram уведомление           | 🔔 подтверждение успешного деплоя |

---

## ✅ Резюме

**Legal Assistant Arbitrage v2.4** может быть развернут:

- через **автоматический CI/CD (GitHub Actions)**
- или вручную по данной инструкции

При ручном деплое гарантируется:

- чистое состояние контейнеров,
- применённые миграции,
- проверенные внешние сервисы,
- и уведомление в Telegram после успешного запуска.

---

🛡️ **Авторизованный деплой должен выполняться только DevOps-инженером или администратором системы.**

```

---

Хочешь, чтобы я подготовил финальный пятый документ —
`docs/ROLLBACK_MANUAL.md`, где будет подробно описано,
как выполнить **откат версии** (rollback) проекта через Docker, Git и Alembic?
```
