"""Compare captured extraction JSON with the anonymized cases, without API calls."""

import json
import sys
from pathlib import Path


def flatten(value, prefix=""):
    if isinstance(value, dict):
        for key, child in value.items():
            yield from flatten(child, f"{prefix}.{key}" if prefix else key)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from flatten(child, f"{prefix}[{index}]")
    else:
        yield prefix, value


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: python tests/eval/evaluate.py ACTUAL_RESULTS_DIR")
        return 2
    actual_directory = Path(sys.argv[1])
    correct = total = 0
    for case_path in sorted(Path(__file__).with_name("cases").glob("*.json")):
        case = json.loads(case_path.read_text())
        actual_path = actual_directory / case_path.name
        if not actual_path.exists():
            print(f"missing: {actual_path}")
            continue
        actual = dict(flatten(json.loads(actual_path.read_text())))
        for field, expected in flatten(case["expected"]):
            total += 1
            correct += actual.get(field) == expected
    print(
        f"field accuracy: {correct}/{total} ({correct / total:.1%})"
        if total
        else "no results"
    )
    return 0 if total else 1


if __name__ == "__main__":
    raise SystemExit(main())
