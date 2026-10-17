from scripts.export_openapi import OPENAPI_PATH, render_openapi


def test_openapi_snapshot_is_current():
    assert OPENAPI_PATH.read_text(encoding="utf-8") == render_openapi()
