import os

from fastapi import APIRouter
from sqlalchemy import text

from backend.app.database import SessionLocal

router = APIRouter()

APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
APP_ENV = os.getenv("APP_ENV", "development")


@router.get("/health")
def health_check():
    status = {
        "status": "ok",
        "version": APP_VERSION,
        "env": APP_ENV,
    }

    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        status["db"] = "connected"
    except Exception as e:
        status["db"] = f"error: {str(e)}"
        status["status"] = "error"

    return status
