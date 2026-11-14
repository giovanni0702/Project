# Single entry point for checks. Quiet: prints failures only.
.PHONY: check test-all

check:
	@python3 scripts/check_docs.py
	@python3 scripts/check_secrets.py
	@if [ -d tests ]; then python3 -m pytest -q -x tests; fi

# Full suite: only at iteration close or before a release.
test-all: check
