# Single entry point for checks. Quiet: prints failures only.
PY := $(shell [ -x .venv/bin/python ] && echo .venv/bin/python || echo python3)
.PHONY: setup check test-all

setup:
	@python3 -m venv .venv && .venv/bin/pip install -q -r requirements.txt

check:
	@$(PY) scripts/check_docs.py
	@$(PY) scripts/check_secrets.py
	@$(PY) -m pytest -q -x tests > .check.log 2>&1 || (cat .check.log; exit 1)

# Full suite: only at iteration close or before a release.
test-all: check
