from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def main():
    # пример: фиксим backend/app/routes/__init__.py
    routes_init = BASE_DIR / "backend" / "app" / "routes" / "__init__.py"
    if routes_init.exists():
        text = routes_init.read_text(encoding="utf-8")
        if "users, laws, decisions, health" in text and "auth" not in text:
            text = text.replace(
                "users, laws, decisions, health",
                "users, laws, decisions, health, auth",
            )
            routes_init.write_text(text, encoding="utf-8")
            print("✅ Added auth to routes/__init__.py")

    # можно добавить и другие фиксы
    print("🎉 fix_v2.py completed")


if __name__ == "__main__":
    main()
