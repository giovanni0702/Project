#!/usr/bin/env python3
"""Minimal secret scan over tracked files. Prints failures only.
Not a replacement for a dedicated scanner; it catches the common mistakes."""
import re
import subprocess
import sys

PATTERNS = {
    "Google API key": r"AIza[0-9A-Za-z_\-]{35}",
    "AWS access key": r"AKIA[0-9A-Z]{16}",
    "private key block": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "GitHub token": r"gh[pousr]_[0-9A-Za-z]{36,}",
    "Slack token": r"xox[baprs]-[0-9A-Za-z\-]{10,}",
    "hard-coded credential": r"(?i)\b(?:api[_-]?key|secret|password|token)\b\s*[:=]\s*[\"'][^\"'\s]{16,}[\"']",
}
FORBIDDEN_FILES = re.compile(r"(^|/)\.env($|\.)|\.(p12|jks|key|pem)$|google-services\.json$|GoogleService-Info\.plist$")

files = subprocess.run(["git", "ls-files"], capture_output=True, text=True, check=True).stdout.split("\n")
errors = []
for name in filter(None, files):
    if FORBIDDEN_FILES.search(name) and not name.endswith(".env.example"):
        errors.append(f"{name}: file type must not be committed")
        continue
    if name == "scripts/check_secrets.py":
        continue
    try:
        text = open(name, encoding="utf-8").read()
    except (UnicodeDecodeError, OSError):
        continue
    for label, pattern in PATTERNS.items():
        if re.search(pattern, text):
            errors.append(f"{name}: possible {label}")

if errors:
    print("\n".join(errors))
    sys.exit(1)
