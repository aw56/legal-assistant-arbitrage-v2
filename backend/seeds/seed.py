import asyncio
from datetime import datetime

from backend.app.core.security import get_password_hash
from backend.app.database import Base, async_session_maker, engine
from backend.app.models.decision import Decision
from backend.app.models.law import Law
from backend.app.models.user import User


async def seed_data():
    async with async_session_maker() as session:
        # Очистка таблиц (для идемпотентности)
        await session.execute("TRUNCATE TABLE decisions RESTART IDENTITY CASCADE;")
        await session.execute("TRUNCATE TABLE laws RESTART IDENTITY CASCADE;")
        await session.execute("TRUNCATE TABLE users RESTART IDENTITY CASCADE;")

        # ================================
        # 👤 Пользователи
        # ================================
        users = [
            User(
                username="admin",
                email="admin@example.com",
                hashed_password=get_password_hash("admin123"),
                role="admin",
            ),
            User(
                username="manager",
                email="manager@example.com",
                hashed_password=get_password_hash("manager123"),
                role="manager",
            ),
            User(
                username="client",
                email="client@example.com",
                hashed_password=get_password_hash("client123"),
                role="client",
            ),
        ]
        session.add_all(users)

        # ================================
        # 📜 Законы
        # ================================
        laws = [
            Law(
                title="Гражданский кодекс РФ",
                content="Основной документ гражданского права РФ",
            ),
            Law(
                title="Арбитражный процессуальный кодекс РФ",
                content="Регламент арбитражного судопроизводства",
            ),
            Law(
                title='Федеральный закон "Об адвокатской деятельности"',
                content="Закон регулирует деятельность адвокатов в РФ",
            ),
        ]
        session.add_all(laws)

        # ================================
        # ⚖️ Судебные решения
        # ================================
        decisions = [
            Decision(
                title="Дело №А40-12345/2025",
                content="Рассмотрение спора по договору поставки.",
            ),
            Decision(
                title="Дело №А40-54321/2025",
                content="Арбитражный спор по аренде нежилого помещения.",
            ),
            Decision(
                title="Дело №А40-67890/2025",
                content="Иск о взыскании задолженности по контракту.",
            ),
        ]
        session.add_all(decisions)

        await session.commit()
        print("🌱 Сиды применены успешно!")


if __name__ == "__main__":
    asyncio.run(seed_data())
