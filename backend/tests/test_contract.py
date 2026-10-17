import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HANDOFF_PATH = ROOT / "specs" / "frontend-handoff.md"
OPENAPI_PATH = ROOT / "openapi.json"


def test_handoff_endpoints_exist_in_openapi():
    handoff = HANDOFF_PATH.read_text(encoding="utf-8")
    endpoints_section = handoff.split("## 5. Endpoints", 1)[1].split("## 6.", 1)[0]
    expected = {
        (method.lower(), f"/v1{path.split('?', 1)[0]}")
        for method, path in re.findall(
            r"^### `([A-Z]+) ([^`]+)`$", endpoints_section, re.MULTILINE
        )
    }
    schema = json.loads(OPENAPI_PATH.read_text(encoding="utf-8"))
    actual = {
        (method, path)
        for path, operations in schema["paths"].items()
        for method in operations
        if method in {"get", "post", "patch", "delete", "put"}
    }

    assert expected <= actual, f"Missing endpoints: {sorted(expected - actual)}"


def test_handoff_error_codes_exist_in_app_source():
    handoff = HANDOFF_PATH.read_text(encoding="utf-8")
    conventions = handoff.split("## 3. Conventions", 1)[1].split("## 4.", 1)[0]
    expected = set(re.findall(r"^\| \d{3} \| `([^`]+)` \|", conventions, re.MULTILINE))
    source = "\n".join(
        path.read_text(encoding="utf-8") for path in (ROOT / "app").rglob("*.py")
    )

    assert not (missing := expected - set(re.findall(r'"([a-z_]+)"', source))), (
        f"Error codes missing from app source: {sorted(missing)}"
    )
