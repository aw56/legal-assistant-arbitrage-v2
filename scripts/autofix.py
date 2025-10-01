#!/usr/bin/env python3
import subprocess
import sys


def run(cmd, check=True):
    print(f"$ {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    if check and result.returncode != 0:
        sys.exit(result.returncode)
    return result


def main():
    print("🚀 Starting autofix...")

    # 1. black
    run(["black", "backend/app", "scripts"])

    # 2. isort
    run(["isort", "backend/app", "scripts"])

    # 3. flake8 (только проверка, без выхода с ошибкой)
    run(["flake8", "backend/app", "scripts"], check=False)

    # 4. pytest
    print("🧪 Running tests...")
    run(
        [
            "docker",
            "compose",
            "-f",
            "docker-compose.prod.yml",
            "exec",
            "backend",
            "pytest",
            "backend/app/tests",
        ],
        check=False,
    )

    print("✅ Autofix and test run complete.")


if __name__ == "__main__":
    main()
