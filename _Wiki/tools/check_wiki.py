"""Check the repository wiki's local links, metadata, and index coverage.

Run with Python 3 from any directory. Only inline Markdown links and a small,
explicit frontmatter convention are checked; this is not a Markdown/YAML parser
or a factual review. The checker never changes files or accesses the network.
"""

from datetime import date
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


WIKI = Path(__file__).resolve().parents[1]
ROOT = WIKI.parent
STATUSES = {"active", "draft", "superseded", "template"}
LINK = re.compile(r"!?\[[^\]\n]+\]\(([^)\n]+)\)")


def prose(text):
    """Exclude fenced examples so placeholder links are not treated as pages."""
    lines = []
    fence = None
    for line in text.splitlines():
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token
            elif token[0] == fence[0] and len(token) >= len(fence):
                fence = None
            continue
        if fence is None:
            lines.append(line)
    return "\n".join(lines)


def metadata_errors(path, text):
    if not text.startswith("---\n"):
        return ["missing frontmatter"]
    parts = text.split("\n---", 1)
    if len(parts) != 2:
        return ["unclosed frontmatter"]
    fields = {}
    for line in parts[0].splitlines()[1:]:
        key, separator, value = line.partition(":")
        if separator:
            fields[key.strip()] = value.strip()
    errors = []
    for key in ("title", "status", "updated"):
        if not fields.get(key):
            errors.append("missing metadata: " + key)
    if fields.get("status") and fields["status"] not in STATUSES:
        errors.append("invalid page status: " + fields["status"])
    if fields.get("updated"):
        try:
            value = fields["updated"]
            if date.fromisoformat(value).isoformat() != value:
                raise ValueError(value)
        except ValueError:
            errors.append("updated must be YYYY-MM-DD")
    return [str(path.relative_to(ROOT)) + ": " + error for error in errors]


def local_links(path, text):
    for match in LINK.finditer(prose(text)):
        destination = match.group(1).strip()
        if destination.startswith("<") and ">" in destination:
            destination = destination[1:destination.index(">")]
        else:
            destination = destination.split(' "', 1)[0]
        parsed = urlsplit(destination)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        yield destination, (path.parent / unquote(parsed.path)).resolve()


def main():
    pages = sorted(WIKI.rglob("*.md"))
    entries = [ROOT / name for name in ("README.md", "AGENTS.md", "CLAUDE.md")]
    errors = []
    index_targets = set()
    checked_links = 0
    for path in pages + entries:
        if not path.is_file():
            errors.append("missing entry point: " + str(path.relative_to(ROOT)))
            continue
        try:
            text = path.read_text(encoding="utf-8-sig")
        except (OSError, UnicodeError) as error:
            errors.append(str(path.relative_to(ROOT)) + ": " + str(error))
            continue
        if path in pages:
            errors.extend(metadata_errors(path, text))
        for destination, target in local_links(path, text):
            checked_links += 1
            if not target.is_relative_to(ROOT):
                errors.append(str(path.relative_to(ROOT)) + ": link escapes repository: " + destination)
            elif not target.exists():
                errors.append(str(path.relative_to(ROOT)) + ": missing link target: " + destination)
            if path == WIKI / "index.md":
                index_targets.add(target)
    for path in pages:
        if path != WIKI / "index.md" and path not in index_targets:
            errors.append("not listed in _Wiki/index.md: " + str(path.relative_to(ROOT)))
    if errors:
        print("FAIL: wiki structural check")
        for error in errors:
            print("- " + error)
        return 1
    print(
        "PASS: {0} wiki pages, {1} entry points, {2} local links; "
        "metadata and index coverage valid.".format(len(pages), len(entries), checked_links)
    )
    print("Not checked: URL availability, heading anchors, factual correctness, or application behavior.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
