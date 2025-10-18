---
title: "Release Operations Guide"
version: "v2.9"
author: "Aleksej — Project Owner"
created: "2025-10-17"
status: "✅ Stable"
description: "Полное руководство по релизному циклу: verify → release-template → finalize (v2.9+)"
---

# 🚀 Release Operations Guide — Legal Assistant Arbitrage v2.9

## 📘 Назначение

Документ описывает **полный DevOps-релизный процесс**  
в рамках Legal Assistant Arbitrage API начиная с версии **v2.9**.  
Все операции стандартизированы через `make` и проходят автоматическую проверку.

> 🧩 Формула релиза:  
> **verify → snapshot → release → finalize → push-safe**

---

## ⚙️ 1. Этапы релизного цикла

| Этап               | Цель                                     | Команда                    | Проверка                  |
| ------------------ | ---------------------------------------- | -------------------------- | ------------------------- |
| **1️⃣ Проверка**    | Предварительная валидация среды и патчей | `make release-verify`      | flake8, patch-verify      |
| **2️⃣ Подготовка**  | Форматирование, автолинт, snapshot       | `make release-template`    | pre-commit + markdownlint |
| **3️⃣ Финализация** | Архивирование и пуш снапшотов            | `make release-finalize`    | snapshot artifacts        |
| **4️⃣ CI sync**     | Проверка CI и тегов                      | `make collaboration-check` | markdownlint, yamllint    |
| **5️⃣ Push-safe**   | Безопасная публикация изменений          | `make safe-push`           | GitHub Actions green      |

---

## 🔍 2. make release-verify

Предназначен для проверки целостности среды перед началом релиза:

```bash
make release-verify version=v2.9
Что делает
Проверяет Python-окружение и зависимости.

Валидирует pre-commit хуки.

Проверяет применимость патча (make patch-verify).

Готовит отчёт о состоянии для CI.

✅ При успешном выполнении:
Verification complete. Ready for release.

🧩 3. make release-template
Основной автоматизированный релизный цикл:

bash
Копировать код
make release-template version=v2.9
Что выполняется
Автоматическое форматирование (black, isort, flake8);

Очистка и пересоздание снапшотов (make snapshot-patches);

Автофикс документации (markdownlint-cli2 --fix);

Создание нового Git-тега с комментарием;

Push в ветку release/v2.9-dev.

✅ Завершение релиза фиксируется сообщением:

sql
Копировать код
✅ Release v2.9 pushed successfully!
🏁 4. make release-finalize
Финальный шаг релиза, создающий артефакты и архивы:

bash
Копировать код
make release-finalize version=v2.9
Что делает
Создаёт полный снапшот в patches/;

Копирует архив в artifacts/patches_snapshot_YYYYMMDD_HHMM/;

Обновляет релизную документацию;

Фиксирует завершение релиза в Telegram (через notifier, если активен).

📦 Пример вывода:

sql
Копировать код
📦 Creating final release snapshot for v2.9...
📄 Snapshot archived.
🏁 Release v2.9 successfully finalized.
🧭 5. Цепочка релизных зависимостей
Файл	Назначение
make/release-template.mk	Основные релизные цели
make/patch-verify.mk	Проверка целостности патчей
docs/MAKE_PATCH_AND_RELEASE_GUIDE_v2.8.md	Исторический контекст и стандарты
docs/RELEASE_OPERATIONS_GUIDE_v2.9.md	Текущее руководство
artifacts/patches_snapshot_*.md	Лог релизов и снапшотов

🔐 6. Релизная безопасность
Контроль	Инструмент	Цель
Secrets	detect-secrets	защита токенов
Docs	markdownlint	чистота документации
Code	flake8, isort, black	соблюдение PEP8
Patches	patch-verify	откат без конфликтов
CI/CD	collaboration-check	валидация контура

📜 7. Пример полного цикла релиза
bash
Копировать код
make release-verify version=v2.9
make release-template version=v2.9
make release-finalize version=v2.9
make collaboration-check
make safe-push
💬 После выполнения ты получаешь:

зеленый CI-поток;

обновлённые артефакты;

чистый релизный снапшот;

релизный тег v2.9 опубликован на GitHub.

🧠 8. Принципы Full Clean Release Mode
Один релиз — один снапшот.

Никаких ручных правок после finalize.

Каждый артефакт проверен и заархивирован.

CI всегда отражает фактическое состояние.

Документация обновляется автоматически.

📅 Последняя ревизия: 2025-10-17
👤 Ответственный: Aleksej (Project Owner)
🧩 Совместимо с: collaboration-check, pre-commit, markdownlint, yamllint

```
