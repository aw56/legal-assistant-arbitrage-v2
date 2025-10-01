import re
from pathlib import Path

VERSIONS_DIR = Path("migrations/versions")

HEADER = '''"""Migration auto-fixed to PEP8/black style."""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
'''

FOOTER = '''

def upgrade() -> None:
    """Apply migration changes."""
    pass


def downgrade() -> None:
    """Revert migration changes."""
    pass
'''


def fix_migration(path: Path):
    text = path.read_text(encoding="utf-8")

    # Убираем старый Alembic хлам и лишние пробелы
    text = re.sub(r'"""[\s\S]*?"""', '"""Auto-formatted migration."""', text, count=1)
    text = re.sub(r" +\n", "\n", text)
    text = re.sub(r"\t", "    ", text)

    # Добавляем header, если его нет
    if "alembic import op" not in text:
        text = HEADER + text

    # Добавляем footer, если нет upgrade/downgrade
    if "def upgrade" not in text:
        text += FOOTER

    path.write_text(text.strip() + "\n", encoding="utf-8")
    print(f"✅ Fixed {path.name}")


def main():
    for pyfile in VERSIONS_DIR.glob("*.py"):
        fix_migration(pyfile)


if __name__ == "__main__":
    main()
