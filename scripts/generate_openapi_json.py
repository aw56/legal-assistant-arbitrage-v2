import json
from pathlib import Path

from fastapi.openapi.utils import get_openapi

from backend.app.main import app

schema = get_openapi(
    title=app.title or "Legal Assistant API",
    version="2.0.0",
    routes=app.routes,
)
out = Path("docs/openapi.json")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(schema, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"OpenAPI saved to {out}")
