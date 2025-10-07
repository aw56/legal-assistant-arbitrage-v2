-- ✅ Фикс Alembic: создать таблицу версий и выставить HEAD
DO $$
BEGIN
    -- если таблицы нет — создаём
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.tables
        WHERE table_name = 'alembic_version'
    ) THEN
        CREATE TABLE alembic_version (
            version_num VARCHAR(32) NOT NULL
        );
    END IF;

    -- очищаем, чтобы не было дубликатов
    DELETE FROM alembic_version;

    -- ⚠️ сюда нужно подставить актуальный head из `alembic heads`
    INSERT INTO alembic_version (version_num) VALUES ('c36040b89d11');
END $$;
