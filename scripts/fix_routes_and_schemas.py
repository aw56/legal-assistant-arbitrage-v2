from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


# --- 1. Routes fix ---
def fix_routes():
    routes_dir = BASE_DIR / "backend" / "app" / "routes"
    for file in ["users.py", "laws.py", "decisions.py"]:
        path = routes_dir / file
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")

        # фикс: переставляем порядок аргументов
        text = text.replace(
            "response_model=schemas.user.User, status_code=201",
            "status_code=201, response_model=schemas.user.User",
        )
        text = text.replace(
            "response_model=schemas.law.Law, status_code=201",
            "status_code=201, response_model=schemas.law.Law",
        )
        text = text.replace(
            "response_model=schemas.decision.Decision, status_code=201",
            "status_code=201, response_model=schemas.decision.Decision",
        )

        path.write_text(text, encoding="utf-8")
        print(f"✅ Fixed {file}")


# --- 2. Schemas fix ---
def fix_user_schema():
    schema_path = BASE_DIR / "backend" / "app" / "schemas" / "user.py"
    if not schema_path.exists():
        return
    text = schema_path.read_text(encoding="utf-8")

    if "ConfigDict" not in text:
        text = "from pydantic import ConfigDict\n" + text

    if "model_config" not in text:
        text = text.replace(
            "class User(BaseModel):",
            "class User(BaseModel):\n    "
            "model_config = ConfigDict(use_enum_values=True)",
        )

    schema_path.write_text(text, encoding="utf-8")
    print("✅ Fixed user.py schema")


# --- 3. Health test fix ---
def fix_test_health():
    test_path = BASE_DIR / "backend" / "app" / "tests" / "test_health.py"
    if not test_path.exists():
        return
    text = """def test_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json().get("status") == "ok"
"""
    test_path.write_text(text, encoding="utf-8")
    print("✅ Fixed test_health.py")


if __name__ == "__main__":
    fix_routes()
    fix_user_schema()
    fix_test_health()
    print("\n🎉 All fixes applied! Now run: make git-fix && make test")
