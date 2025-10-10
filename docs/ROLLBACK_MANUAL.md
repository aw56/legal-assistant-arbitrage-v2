Прекрасно 💾
Вот завершающий документ — **`docs/ROLLBACK_MANUAL.md`**,
в котором подробно описано, как выполнить безопасный **откат версии (rollback)**
в проекте **Legal Assistant Arbitrage v2.4**.

Он предназначен для DevOps-инженеров и системных администраторов,
чтобы в случае сбоя на продакшне можно было быстро восстановить рабочее состояние приложения.

---

````markdown
# 🔄 ROLLBACK MANUAL — Legal Assistant Arbitrage v2.4

## 📘 Назначение

Этот документ описывает процедуры **отката версии приложения**, **базы данных** и **Docker-образов**
для проекта **Legal Assistant Arbitrage v2.4**.
Откат выполняется при ошибках после деплоя, некорректных миграциях или проблемах в CI/CD пайплайне.

---

## ⚠️ 1. Когда требуется rollback

| Ситуация                            | Признаки                                      |
| ----------------------------------- | --------------------------------------------- |
| Ошибка деплоя                       | Telegram-уведомление ❌ «Ошибка деплоя»       |
| Несовместимая миграция              | Alembic `upgrade head` вызывает исключение    |
| Падение backend-контейнера          | `docker logs backend` содержит ошибки запуска |
| API недоступно                      | `/api/health` возвращает ошибку               |
| Telegram/KAD интеграции не проходят | CI падает на этапе integration                |

---

## 🧠 2. Принцип отката

Rollback выполняется **в двух слоях**:

1. **Код / Docker-образ**
   - откат к предыдущему тэгу (например, `v2.3`);
2. **База данных**
   - откат миграции Alembic к предыдущей ревизии.

---

## 🧱 3. Проверка текущего состояния

### Проверка текущего git-коммита

```bash
git log -1 --oneline
```
````

### Проверка версии Docker-образа

```bash
docker images | grep legal-assistant-backend
```

Пример:

```
ghcr.io/aw56/legal-assistant-backend   v2.4   123abc45   2 hours ago
```

---

## 📦 4. Откат к предыдущему Docker-образу

### Найди нужный тэг

```bash
docker pull ghcr.io/aw56/legal-assistant-backend:v2.3
```

### Перезапусти backend с нужной версией

```bash
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d --force-recreate --build
```

или вручную указав версию:

```bash
docker run -d --name legal-assistant-backend \
  -p 8080:8080 \
  ghcr.io/aw56/legal-assistant-backend:v2.3
```

---

## 🗄️ 5. Откат миграций Alembic

### Проверить список ревизий

```bash
docker compose -f docker-compose.prod.yml exec -T backend alembic history
```

### Проверить текущую миграцию

```bash
docker compose -f docker-compose.prod.yml exec -T backend alembic current
```

### Откатить на предыдущую ревизию

```bash
docker compose -f docker-compose.prod.yml exec -T backend alembic downgrade -1
```

или указать конкретный revision ID:

```bash
docker compose -f docker-compose.prod.yml exec -T backend alembic downgrade <revision_id>
```

### Проверить актуальное состояние

```bash
docker compose -f docker-compose.prod.yml exec -T backend alembic current
```

---

## 💾 6. Восстановление базы данных из бэкапа

Если откат миграции невозможен (например, сломанные зависимости между таблицами):

```bash
cat artifacts/db_backup_2025_10_09.sql | docker exec -i legal-assistant-db psql -U admin -d legal_assistant_db
```

После восстановления — обязательно прогоните smoke-тест:

```bash
make smoke-local
```

---

## 🔁 7. Проверка после отката

### Проверка API

```bash
curl -s http://127.0.0.1:8080/api/health | jq
```

Ожидаемый результат:

```json
{ "status": "ok" }
```

### Проверка Telegram-интеграции

```bash
make telegram-notify-test
```

Ожидается сообщение:

> 🧩 Rollback Test: Telegram connection OK ✅

### Проверка версии backend

```bash
docker exec -it legal-assistant-backend python -c "import backend; print(backend.__version__)"
```

---

## 🧰 8. Отправка уведомления об откате

После успешного восстановления выполните:

```bash
python3 backend/app/utils/notify_telegram.py "♻️ Откат выполнен: Legal Assistant Arbitrage v2.4 → v2.3 успешно завершён ✅"
```

Если откат не удался:

```bash
python3 backend/app/utils/notify_telegram.py "🚨 Ошибка при откате версии Legal Assistant Arbitrage — требуется вмешательство DevOps ❌"
```

---

## 🩺 9. Полный сценарий аварийного восстановления

```bash
# 1. Подключаемся к серверу
ssh -i ~/.ssh/prod_legal_assistant.pem user@server-ip

# 2. Проверяем контейнеры
docker compose -f docker-compose.prod.yml ps

# 3. Делаем резервный бэкап
docker exec -t legal-assistant-db pg_dump -U admin legal_assistant_db > artifacts/rollback_backup_$(date +'%Y%m%d_%H%M%S').sql

# 4. Откатываем миграции
docker compose -f docker-compose.prod.yml exec -T backend alembic downgrade -1

# 5. Перезапускаем backend на предыдущем образе
docker pull ghcr.io/aw56/legal-assistant-backend:v2.3
docker compose -f docker-compose.prod.yml up -d --force-recreate

# 6. Проверяем API и Telegram
make smoke-local
make telegram-notify-test
```

---

## 🧾 10. Чеклист rollback-а

| Этап                     | Команда                        | Ожидаемый результат           |
| ------------------------ | ------------------------------ | ----------------------------- |
| Проверить текущую версию | `git log -1 --oneline`         | версия v2.4                   |
| Выбрать образ            | `docker pull ghcr.io/...:v2.3` | загрузка прошла успешно       |
| Откат миграций           | `alembic downgrade -1`         | миграция откатана             |
| Smoke-тест               | `make smoke-local`             | ✅ API доступен               |
| Проверка Telegram        | `make telegram-notify-test`    | уведомление получено          |
| Telegram alert           | `notify_telegram.py`           | сообщение “Rollback выполнен” |

---

## 🔐 11. Предупреждения и ограничения

- Никогда не выполняй rollback **в середине деплоя** — дождись завершения CI.
- После отката обязательно пересоздай бэкап новой (старой) стабильной версии.
- При откате БД всегда сохраняй резервную копию перед `downgrade` или восстановлением.
- Все rollback-и должны фиксироваться в `CHANGELOG.md` или `docs/DEPLOY_LOG.md`.

---

## 🧩 12. Пример уведомления о rollback-е

> ♻️ **Rollback выполнен успешно**
>
> 📦 Версия: `v2.4 → v2.3`
> ⚙️ Миграции откатаны
> 🌐 API отвечает `/health: ok`
> 📅 Дата: 2025-10-09
> 👤 Исполнитель: `admin@legal-assistant`

---

## ✅ Резюме

Rollback в **Legal Assistant Arbitrage v2.4** — безопасный и управляемый процесс.
Он включает:

- откат Docker-образа,
- откат миграций Alembic,
- восстановление БД из бэкапа,
- проверку интеграций (Telegram, KAD),
- и уведомление в Telegram.

После успешного отката обязательно выполнить:

```bash
make doctor
```

чтобы убедиться, что окружение полностью стабильно.

---

🛡️ **Rollback рекомендуется проводить только DevOps-инженеру или администратору**,
после подтверждения от технического лида или владельца проекта.

```

---

Хочешь, чтобы я подготовил завершающий файл `docs/DEPLOY_LOG_TEMPLATE.md` —
шаблон журнала для фиксирования всех деплоев и откатов (дата, версия, ветка, исполнитель, результат)?
```
