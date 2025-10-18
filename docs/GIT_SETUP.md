
---
title: "Git Setup & Подключение к GitHub"
version: "v2.9.7"
author: "Aleksej — Project Owner"
updated: "2025-10-16"
status: "✅ Lint-Clean"
description: "Единая инструкция по настройке Git и подключению к GitHub для Legal Assistant Arbitrage"
---

# 🛠 Git setup & подключение к GitHub

## 📌 Настройка Git (один раз)

Задаём имя и email (рекомендуется GitHub **noreply email**):

```bash
git config --global user.name "Aleksej Walz"
git config --global user.email "37653309+aw56@users.noreply.github.com"
```

Проверяем:

```bash
git config --list | grep -E "^user\."
```

Ожидаемый вывод:

```
user.name=Aleksej Walz
user.email=37653309+aw56@users.noreply.github.com
```

---

## 🔑 SSH-ключ для GitHub

1. Проверяем наличие ключей:

   ```bash
   ls -al ~/.ssh
   ```

2. Создаём ключ (если отсутствует):

   ```bash
   ssh-keygen -t ed25519 -C "37653309+aw56@users.noreply.github.com"
   ```

3. Запускаем агент и добавляем ключ:

   ```bash
   eval "$(ssh-agent -s)"
   ssh-add ~/.ssh/id_ed25519
   ```

4. Копируем публичный ключ:

   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

5. Добавляем ключ в GitHub:
   Settings → **SSH and GPG keys** → **New SSH key** → вставляем содержимое.

6. Проверяем соединение:

   ```bash
   ssh -T git@github.com
   ```

   Успешный ответ:

   ```
   Hi aw56! You've successfully authenticated, but GitHub does not provide shell access.
   ```

---

## 🔗 Подключение репозитория

1. Создаём новый репозиторий на GitHub: [https://github.com/new](https://github.com/new)
   Имя: `legal-assistant-arbitrage-v2`

2. Привязываем `origin`:

   ```bash
   git remote add origin git@github.com:aw56/legal-assistant-arbitrage-v2.git
   ```

3. Первый пуш:

   ```bash
   git branch -M main
   git push -u origin main
   ```

---

## ✅ Best practices

- Коммиты маленькие и атомарные.
- Сообщения в стиле Conventional Commits:
  - `feat:` — новая функциональность
  - `fix:` — исправление бага
  - `chore:` — поддерживающие изменения
  - `docs:` — документация
  - `test:` — тесты

- Работать в отдельных ветках (`feature/...`, `fix/...`) и открывать Pull Request.

---

## 🧪 Быстрый чек

```bash
git --version
git remote -v
git config --get user.name
git config --get user.email
ssh -T git@github.com
```

---

📅 Последняя ревизия: 2025-10-16
👤 Ответственный: **Aleksej (Project Owner)**
