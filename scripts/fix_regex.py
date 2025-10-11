#!/usr/bin/env python3
r"""
🔧 Авто-фикс регулярных выражений в проекте.
Заменяет строки вида "\\d", "\\(" и т.д. на raw-строки (r"...").
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
EXCLUDE_DIRS = {"venv", ".git", "__pycache__", "migrations"}

# Подозрительные escape-последовательности (в строках)
ESCAPE_PATTERNS = [
    r"\\d",
    r"\\.",
    r"\\(",
    r"\\)",
    r"\\+",
    r"\\*",
    r"\\s",
    r"\\w",
]


def should_skip(path: Path) -> bool:
    """Пропускаем ненужные директории."""
    return any(part in EXCLUDE_DIRS for part in path.parts)


def fix_file(path: Path) -> None:
    """Исправляет строки с неэкранированными regex."""
    text = path.read_text(encoding="utf-8")
    new_lines = []
    changed = False

    for line in text.splitlines():
        if '"' in line or "'" in line:
            for esc in ESCAPE_PATTERNS:
                if esc in line and "r'" not in line and 'r"' not in line:
                    # добавляем r перед кавычкой
                    line = line.replace(f'"{esc}', f'r"{esc}')
                    line = line.replace(f"'{esc}", f"r'{esc}")
                    changed = True
        new_lines.append(line)

    if changed:
        path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
        print(f"✅ Fixed regex in {path}")


def main() -> None:
    for path in BASE_DIR.rglob("*.py"):
        if should_skip(path):
            continue
        fix_file(path)
    print("\n🎉 Regex авто-фикс завершён!")


if __name__ == "__main__":
    main()
