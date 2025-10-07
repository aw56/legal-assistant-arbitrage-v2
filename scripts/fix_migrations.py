#!/usr/bin/env python3
"""
⚡ Авто-фикс Alembic миграций:
1. Проверяет наличие нескольких head-ревизий
2. Если их больше одной → делает merge
3. Ставит метку head в БД (alembic stamp head)
4. Чинит импорты postgresql и добавляет checkfirst=True для ENUM
"""

import subprocess
import sys
from pathlib import Path


def run_cmd(cmd):
    try:
        result = subprocess.run(
            cmd, shell=True, text=True, capture_output=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка при выполнении: {cmd}")
        print(e.stderr)
        sys.exit(1)


def fix_postgresql_imports(migrations_dir="migrations/versions"):
    """Добавляем импорт postgresql и checkfirst=True"""
    path = Path(migrations_dir)
    if not path.exists():
        print("⚠️ Нет директории migrations/versions, пропускаем автофикс")
        return

    for file in path.glob("*.py"):
        text = file.read_text()

        changed = False

        # --- fix импорт ---
        if (
            "postgresql." in text
            and "from sqlalchemy.dialects import postgresql" not in text
        ):
            lines = text.splitlines()
            for i, line in enumerate(lines):
                if line.startswith("import sqlalchemy as sa"):
                    lines.insert(
                        i + 1, "from sqlalchemy.dialects import postgresql  # auto-fix"
                    )
                    changed = True
                    break
            text = "\n".join(lines)

        # --- fix checkfirst для ENUM ---
        if (
            "postgresql.ENUM" in text
            and ".create(" in text
            and "checkfirst=True" not in text
        ):
            text = text.replace(".create(", ".create(op.get_bind(), checkfirst=True, ")
            changed = True

        if changed:
            file.write_text(text)
            print(f"✅ Fixed {file.name}")


def main():
    print("🔎 Проверка heads Alembic...")
    heads = run_cmd("alembic heads")
    lines = [line.split()[0] for line in heads.splitlines() if line.strip()]
    print(f"📌 Найдено head-ревизий: {lines}")

    if len(lines) > 1:
        merge_cmd = f"alembic merge -m 'merge heads' {' '.join(lines)}"
        print(f"⚡ Несколько heads → выполняем merge:\n   {merge_cmd}")
        run_cmd(merge_cmd)
    else:
        print("✅ Только один head, merge не нужен")

    # --- автофикс postgresql ---
    fix_postgresql_imports()

    print("📌 Ставим stamp head...")
    run_cmd("alembic stamp head")
    print("🎉 Alembic миграции приведены в порядок!")


if __name__ == "__main__":
    main()
