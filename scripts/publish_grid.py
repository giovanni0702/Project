#!/usr/bin/env python3
"""Publish the static grid for a city. Run every `publish.interval_minutes`.
Usage: scripts/publish_grid.py <city_id> [out_dir]
Until an event store exists it publishes the prior only (low reliability)."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from parking_core.config import load_city  # noqa: E402
from parking_core.publish import build_grid, write_grid  # noqa: E402

city = load_city(sys.argv[1])
out = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "build/grid")
path = write_grid(build_grid(city, outcomes=[]), out)
print(f"{path} {path.stat().st_size} bytes")
