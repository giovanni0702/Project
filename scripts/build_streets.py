#!/usr/bin/env python3
"""Build the static street file for a city through its adapter (D-021).
Usage: scripts/build_streets.py <city_id>  ->  build/streets/<city_id>/streets.json"""
import importlib
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from parking_core import grid, streets  # noqa: E402
from parking_core.config import load_city  # noqa: E402

city = load_city(sys.argv[1])
adapter = importlib.import_module(f"cities.{city['id']}.adapter")
resolution = city["grid"]["h3_resolution"]
pieces = streets.pieces_from_lines(adapter.street_lines(), resolution)
out = ROOT / "build" / "streets" / city["id"] / "streets.json"
out.parent.mkdir(parents=True, exist_ok=True)
payload = {"city": city["id"], "attribution": adapter.ATTRIBUTION, "pieces": pieces}
out.write_text(json.dumps(payload, separators=(",", ":"), ensure_ascii=False), encoding="utf-8")
cells = grid.cells_for_bbox(city["grid"]["bbox"], resolution)
named = sum(1 for p in pieces if p["name"])
print(json.dumps({"file": str(out.relative_to(ROOT)), "bytes": out.stat().st_size,
                  "named_pieces": round(named / len(pieces), 3), "street_cells": len({p["cell"] for p in pieces}),
                  **streets.summary(pieces, cells)}))
