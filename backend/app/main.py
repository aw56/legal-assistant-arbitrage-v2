from fastapi import FastAPI
from backend.app.routes import users, laws, decisions
from backend.app.database import Base, engine

# Создаём таблицы (для SQLite)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Legal Assistant API")

@app.get("/health")
def health():
    return {"status": "ok"}

# Подключаем роутеры
app.include_router(users.router)
app.include_router(laws.router)
app.include_router(decisions.router)
