import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

OPENAPI_PATH = ROOT / "openapi.json"


def render_openapi() -> str:
    from app.main import create_app

    return json.dumps(create_app().openapi(), indent=2, sort_keys=True) + "\n"


if __name__ == "__main__":
    OPENAPI_PATH.write_text(render_openapi(), encoding="utf-8")
