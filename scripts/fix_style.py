#!/usr/bin/env python3
"""
🔧 Fix style: black + isort + flake8 для проекта Legal Assistant v2
"""

import subprocess
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def run_cmd(cmd: list[str]) -> int:
    """Запуск shell-команды с выводом."""
    print(f"\n👉 {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=BASE_DIR)
    return result.returncode


def main() -> None:
    print("⚡ Авто-стилизация кода (black + isort + flake8)\n")

    # Автоформатирование
    rc_black = run_cmd(["black", "."])
    rc_isort = run_cmd(["isort", "."])

    # Проверка
    rc_flake = run_cmd(["flake8", "."])

    if all(code == 0 for code in [rc_black, rc_isort, rc_flake]):
        print("\n✅ Все проверки пройдены (black, isort, flake8)")
    else:
        print("\n⚠️ Есть предупреждения/ошибки — см. выше.")
        sys.exit(1)


if __name__ == "__main__":
    main()
