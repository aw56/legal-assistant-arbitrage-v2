import re
from pathlib import Path

# Базовая директория проекта
BASE_DIR = Path(__file__).resolve().parent.parent
APP_DIR = BASE_DIR / "backend" / "app"


# Замена .dict() → .model_dump()
def replace_dict_to_model_dump(text: str) -> str:
    return re.sub(r"\.dict\(\)", ".model_dump()", text)


# Замена class Config → model_config = ConfigDict(...)
def replace_config(text: str) -> str:
    # Импорт ConfigDict, если он нужен
    if "class Config" in text and "ConfigDict" not in text:
        text = "from pydantic import ConfigDict\n\n" + text
    # Замена блока class Config
    text = re.sub(
        r"class Config:\n\s*orm_mode\s*=\s*True",
        "model_config = ConfigDict(from_attributes=True)",
        text,
    )
    return text


def process_file(file_path: Path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    original = content
    content = replace_dict_to_model_dump(content)
    content = replace_config(content)

    if content != original:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ Updated: {file_path}")


def main():
    print("🔄 Migrating Pydantic v1 → v2 ...")
    for py_file in APP_DIR.rglob("*.py"):
        process_file(py_file)
    print("✨ Migration complete!")


if __name__ == "__main__":
    main()
