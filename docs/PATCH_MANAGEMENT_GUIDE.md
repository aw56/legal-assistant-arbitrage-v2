# 🧩 Патчи (Patch Management Guide)

## Legal Assistant Arbitrage v2.4 — безопасная система снимков

Эта шпаргалка описывает, как **создавать, проверять и хранить патчи** без изменений в рабочем коде.
Патчи фиксируют все текущие правки и позволяют позже восстановить систему из любого состояния.

---

## 1️⃣ Создание патчей (snapshot без применения)

> Все патчи сохраняются в папку `patches/`.
> Команда `git diff` не изменяет проект.

### 🔹 Примеры команд

```bash
# DevOps и Makefile
git diff HEAD Makefile docs/DEVOPS_* > patches/v2.4_devops_docs_HEAD.patch

# Redis + Aggregator Service
git diff HEAD backend/app/services/integrations_service.py \
  > patches/v2.4_integrations_redis_fix_HEAD.patch

# Laws Search Router
git diff HEAD backend/app/routes/laws_search.py \
  > patches/v2.4_laws_search_fix_HEAD.patch

# Полный snapshot проекта
git diff origin/main > patches/v2.4_full_snapshot_$(date +%Y%m%d).patch
```

---

## 2️⃣ Проверка патча без применения

> Проверка выполняется **в сухом режиме** — никаких файлов не изменяется.

```bash
for f in patches/*.patch; do
  echo "🧪 Checking $f"
  git apply --check "$f" || echo "⚠️  $f cannot be applied cleanly"
done
```

Если появляется ошибка `patch does not apply` — значит проект уже обновлён,
и патч относится к старой версии (можно оставить его для архива).

---

## 3️⃣ Хранение и структура

### 📂 Структура каталога `patches/`

```
patches/
│
├── _old/                           # архив старых патчей
│   ├── v2.3_xxx.patch
│   ├── hotfix_20250929.patch
│   └── ...
│
├── v2.4_integrations_redis_fix_HEAD.patch
├── v2.4_laws_search_fix_HEAD.patch
├── v2.4_devops_docs_HEAD.patch
└── v2.4_full_snapshot_20251012.patch
```

### 💾 Рекомендации

- Каждый патч именуй по шаблону:
  `v<версия>_<модуль>_<тип_изменения>_<опционально:HEAD/дата>.patch`

- После успешного релиза:
  переноси старые патчи в `patches/_old/`.

- Для архивации всех патчей можно сделать бэкап:

  ```bash
  tar -czf artifacts/patches_backup_$(date +%Y%m%d).tar.gz patches/
  ```

---

## 4️⃣ Применение патча вручную (только при необходимости)

> ⚠️ Выполняй только осознанно, когда нужно вернуть изменения из snapshot.

```bash
git apply patches/v2.4_laws_search_fix_HEAD.patch
```

Если появятся конфликты, git предложит исправить вручную —
но текущая система остаётся безопасной, пока не выполняется `apply`.

---

## 5️⃣ Автоматизированная проверка всех патчей (Makefile)

Добавь в `Makefile` задачу:

```makefile
patch-check:
 @for f in patches/*.patch; do \
  echo "🧩 Checking $$f"; \
  git apply --check "$$f" || echo "⚠️  $$f failed"; \
 done
```

Теперь можно просто запустить:

```bash
make patch-check
```

---

## ✅ Результат

После выполнения:

- Все патчи зафиксированы и готовы к переносу.
- Проект остаётся неизменным.
- Ты имеешь полный архив состояния v2.4 (Makefile, Redis, Laws Search и DevOps).

---

### 📜 Автор

Aleksej Walz — Legal Assistant Arbitrage v2 maintainer
📅 Обновлено: 2025-10-12

```

---
```
