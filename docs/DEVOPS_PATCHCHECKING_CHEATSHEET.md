# 🧩 Шпаргалка: Проверка и тестирование патчей в Legal Assistant Arbitrage v2

## ⚙️ 1. Проверка применимости патча (без развёртывания)

Проверяет, можно ли применить патч без конфликтов — ничего не меняет в коде.

```bash
git apply --check patches/имя_патча.patch
```

✅ **Пустой вывод** — значит патч применим.
⚠️ **Ошибки** — значит, контекст патча не совпадает с актуальным кодом.

---

## 📊 2. Просмотр, какие файлы изменяет патч

Показывает сводку по затронутым файлам и количеству строк.

```bash
git apply --stat patches/имя_патча.patch
```

💡 Пример вывода:

```
 backend/app/services/integrations_service.py | 25 ++++++++++++++++---------
 1 file changed, 17 insertions(+), 8 deletions(-)
```

---

## 🧪 3. Симуляция применения патча (dry-run staging)

Позволяет временно "примерить" изменения, не изменяя файлы в рабочей директории.

```bash
git apply --index --verbose patches/имя_патча.patch
git diff --cached | less
```

После проверки — **откатить staging без потерь**:

```bash
git reset
```

---

## 🔍 4. Сравнение содержимого патча перед применением

Показывает diff внутри самого `.patch` файла.

```bash
cat patches/имя_патча.patch | less
```

или в более читаемом виде:

```bash
git apply --stat --summary patches/имя_патча.patch
```

---

## 🧰 5. Применение патча (если всё чисто)

Когда убедился, что конфликтов нет — применяешь:

```bash
git apply patches/имя_патча.patch
```

Проверяешь результат:

```bash
git diff
```

---

## 🔄 6. Отмена уже применённого патча

Если нужно вернуть код в исходное состояние:

```bash
git apply -R patches/имя_патча.patch
```

---

## 🚀 7. Пример полного цикла

```bash
cd ~/my_projects/legal-assistant-arbitrage-v2
git pull origin main
git apply --check patches/20251012_aggregator_redis_fix.patch
git apply --stat patches/20251012_aggregator_redis_fix.patch
git apply patches/20251012_aggregator_redis_fix.patch
pytest -q -k "laws_search"
```

---

## 📘 Примечания

- Папка для патчей: `patches/`
- Все патчи фиксируются в `artifacts/PROGRESS_YYYYMMDD_HHMM.md`
- В CI патчи применяются **в тестовом контейнере**, не в основной ветке.
- Для отката можно использовать `make rollback` или `git reset --hard HEAD`.

---

🧩 _Legal Assistant Arbitrage v2 — DevOps Practical Tools © 2025 Aleksej Walz_

```

---

Хочешь, я оформлю это сразу в готовый файл `docs/DEVOPS_CHEATSHEET.md` с автоматической ссылкой из твоего `COMMANDS.md` и добавлением в Makefile (`make cheatsheet`)?
```
