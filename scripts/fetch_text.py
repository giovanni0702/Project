#!/usr/bin/env python3
"""Fetch a web page through the session proxy and save it as plain text.

Use when WebFetch cannot reach an allowed host. Then Grep the saved file
instead of reading it whole.
Usage: scripts/fetch_text.py <url> [name]   ->  data/cache/web/<name>.txt
"""
import html
import pathlib
import re
import subprocess
import sys

url = sys.argv[1]
name = sys.argv[2] if len(sys.argv) > 2 else re.sub(r"[^a-z0-9]+", "-", url.lower())[:80].strip("-")
out = pathlib.Path(__file__).resolve().parent.parent / "data" / "cache" / "web" / f"{name}.txt"
out.parent.mkdir(parents=True, exist_ok=True)
raw = subprocess.run(
    ["curl", "-sL", "-m", "30", "-A", "Mozilla/5.0", url], capture_output=True, check=True
).stdout.decode("utf-8", "replace")
if not raw.lstrip().startswith(("{", "[")):  # keep JSON as is
    raw = re.sub(r"(?s)<(script|style)[^>]*>.*?</\1>", " ", raw)
    raw = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", raw)))
out.write_text(raw, encoding="utf-8")
print(f"{out.relative_to(out.parents[3])} {len(raw)} chars")
