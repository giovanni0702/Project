#!/usr/bin/env python3
"""Project hygiene checks: file length limits, agent description length,
and diverging key values across documents. Prints failures only."""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LIMITS = {"CLAUDE.md": 100, "TASKS.md": 150, "docs/STATO.md": 40}
DOC_LIMIT = 300
DESC_WORDS = 25
# Each key value must be identical wherever it is stated.
KEY_VALUES = {
    "k-anonymity threshold": r"\bk\s*(?:=|≥|>=)\s*(\d+)",
    "raw event retention (days)": r"(?:massimo|max)\s+(\d+)\s+giorni",
}

errors = []
docs = sorted(ROOT.glob("docs/*.md")) + [ROOT / "CLAUDE.md", ROOT / "TASKS.md"]

for path in docs:
    rel = path.relative_to(ROOT).as_posix()
    lines = path.read_text(encoding="utf-8").count("\n")
    limit = LIMITS.get(rel, DOC_LIMIT)
    if lines > limit:
        errors.append(f"{rel}: {lines} lines (limit {limit})")

for path in sorted(ROOT.glob(".claude/agents/*.md")):
    match = re.search(r"^description:\s*(.+)$", path.read_text(encoding="utf-8"), re.M)
    if not match:
        errors.append(f"{path.name}: missing description")
    elif len(match.group(1).split()) > DESC_WORDS:
        errors.append(f"{path.name}: description over {DESC_WORDS} words")

for label, pattern in KEY_VALUES.items():
    seen = {}
    for path in docs:
        for value in re.findall(pattern, path.read_text(encoding="utf-8")):
            seen.setdefault(value, path.relative_to(ROOT).as_posix())
    if len(seen) > 1:
        errors.append(f"diverging {label}: {seen}")

for name in ("docs/STATO.md", "docs/INDICE.md", "docs/fonti.md"):
    if not (ROOT / name).exists():
        errors.append(f"missing {name}")

if errors:
    print("\n".join(errors))
    sys.exit(1)
