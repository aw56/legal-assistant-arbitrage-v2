-- fix_alembic.sql
-- 📌 Ручная синхронизация Alembic без пересоздания таблиц

-- Создаём таблицу версий, если её ещё нет
CREATE TABLE IF NOT EXISTS alembic_version (
    version_num VARCHAR(32) NOT NULL
);

-- Удаляем старые версии (если есть)
TRUNCATE alembic_version;

-- Устанавливаем последнюю миграцию как применённую
INSERT INTO alembic_version (version_num) VALUES ('c36040b89d11');
