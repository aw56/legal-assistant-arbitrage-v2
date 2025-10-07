#!/usr/bin/env python3
"""
⚡ Автофикс Alembic миграций: добавление создания и удаления ENUM userrole.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MIGRATIONS_DIR = BASE_DIR / "migrations" / "versions"


def fix_enum_in_migration(path: Path):
    text = path.read_text(encoding="utf-8")

    if "userrole" not in text:
        return False  # миграция не затрагивает userrole

    fixed = False

    # --- Импорт postgresql ---
    if "from sqlalchemy.dialects import postgresql" not in text:
        text = text.replace(
            "import sqlalchemy as sa",
            "import sqlalchemy as sa\nfrom sqlalchemy.dialects import postgresql",
        )
        fixed = True

    # --- Добавляем userrole_enum.create в upgrade() ---
    if "userrole_enum.create" not in text and "def upgrade()" in text:
        before = "def upgrade() -> None:\n"
        insert = (
            "def upgrade() -> None:\n"
            "    userrole_enum = postgresql.ENUM('admin', 'lawyer', 'user', 'client', name='userrole')\n"
            "    userrole_enum.create(op.get_bind(), checkfirst=True)\n\n"
        )
        text = text.replace(before, insert)
        fixed = True

    # --- Добавляем userrole_enum.drop в downgrade() ---
    if "userrole_enum.drop" not in text and "def downgrade()" in text:
        before = "def downgrade() -> None:\n"
        insert = (
            "def downgrade() -> None:\n"
            "    userrole_enum = postgresql.ENUM('admin', 'lawyer', 'user', 'client', name='userrole')\n"
            "    userrole_enum.drop(op.get_bind(), checkfirst=True)\n\n"
        )
        text = text.replace(before, insert)
        fixed = True

    if fixed:
        path.write_text(text, encoding="utf-8")
        print(f"✅ Fixed ENUM in {path.name}")
        return True

    return False


def main():
    if not MIGRATIONS_DIR.exists():
        print("❌ Migrations directory not found")
        return

    fixed_files = 0
    for path in MIGRATIONS_DIR.glob("*.py"):
        if fix_enum_in_migration(path):
            fixed_files += 1

    if fixed_files == 0:
        print("ℹ️ No migrations required fixing")
    else:
        print(f"\n🎉 Fixed {fixed_files} migration file(s). Now run: make migrate")


if __name__ == "__main__":
    main()
