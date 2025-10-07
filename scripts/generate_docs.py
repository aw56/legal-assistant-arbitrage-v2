import sys
from pathlib import Path

from backend.app.main import app

OUTPUT_FILE = Path("docs/API_DOCS.md")


def main():
    try:
        spec = app.openapi()
    except Exception as e:
        sys.stderr.write(f"❌ Ошибка генерации OpenAPI схемы: {e}\n")
        sys.exit(1)

    md: list[str] = []
    md.append("# 📖 API Docs — Legal Assistant Arbitrage v2\n")
    md.append("Сгенерировано автоматически из FastAPI OpenAPI схемы\n\n")

    for path, methods in spec.get("paths", {}).items():
        md.append(f"## `{path}`\n")
        for method, details in methods.items():
            summary = details.get("summary", "")
            md.append(f"### {method.upper()}\n")
            md.append(f"- **Описание:** {summary}\n")

            if "parameters" in details:
                md.append("#### Параметры:\n")
                for p in details["parameters"]:
                    md.append(
                        f"- `{p['name']}` ({p['in']}): {p.get('description', '')}"
                    )

            if "requestBody" in details:
                md.append("#### Тело запроса:\n")
                md.append("```json\nпример данных...\n```\n")

            if "responses" in details:
                md.append("#### Ответы:\n")
                for code, resp in details["responses"].items():
                    desc = resp.get("description", "")
                    md.append(f"- `{code}`: {desc}")
            md.append("\n")

    OUTPUT_FILE.write_text("\n".join(md), encoding="utf-8")
    print(f"✅ Документация сохранена в {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
