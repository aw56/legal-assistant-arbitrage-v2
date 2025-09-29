import json
import os
import sys

from fastapi.openapi.utils import get_openapi

# Добавляем корень проекта в sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from backend.app.main import app  # noqa: E402


def generate_docs():
    """Генерация OpenAPI схемы и запись в docs/API_DOCS.md"""
    openapi_schema = get_openapi(
        title=app.title,
        version="1.0.0",
        description="Legal Assistant Arbitrage API",
        routes=app.routes,
    )

    output_path = os.path.join("docs", "API_DOCS.md")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("# 📖 API Documentation\n\n")
        f.write("```json\n")
        f.write(json.dumps(openapi_schema, indent=2, ensure_ascii=False))
        f.write("\n```")

    print(f"✅ OpenAPI docs сгенерированы: {output_path}")


if __name__ == "__main__":
    generate_docs()
