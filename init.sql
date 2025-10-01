-- alembic_version
CREATE TABLE IF NOT EXISTS alembic_version (
    version_num VARCHAR(32) NOT NULL PRIMARY KEY
);

-- вставляем только если нет такой версии
INSERT INTO alembic_version (version_num)
VALUES ('735e1b23daa0')
ON CONFLICT (version_num) DO NOTHING;

-- users
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL,
    role VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- laws
CREATE TABLE IF NOT EXISTS laws (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- decisions
CREATE TABLE IF NOT EXISTS decisions (
    id SERIAL PRIMARY KEY,
    law_id INT REFERENCES laws(id) ON DELETE CASCADE,
    decision TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- тестовый пользователь
INSERT INTO users (username, password, role)
VALUES ('alice', 'secret', 'client')
ON CONFLICT (username) DO NOTHING;
