# --- Базовый образ ---
FROM python:3.12-slim

# --- Переменные окружения ---
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# --- Устанавливаем зависимости системы ---
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    netcat-openbsd \
    wget \
    && rm -rf /var/lib/apt/lists/*

# --- Рабочая директория ---
WORKDIR /code

# --- Устанавливаем Python зависимости ---
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    pip install alembic psycopg2-binary

# --- Копируем проект ---
COPY . .

# --- Скрипты ---
RUN chmod +x /code/wait-for-db.sh /code/entrypoint.sh || true

# --- Точка входа ---
ENTRYPOINT ["/code/entrypoint.sh"]
