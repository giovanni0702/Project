#!/usr/bin/env python3
"""Build the static street file for a city from the raw OSM download.
Usage: scripts/build_streets.py <city_id>  ->  build/streets/<city_id>/streets.json"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from parking_core import grid, streets  # noqa: E402
from parking_core.config import load_city  # noqa: E402

city = load_city(sys.argv[1])
raw = json.loads((ROOT / "data" / "raw" / city["id"] / "osm_streets.json").read_text(encoding="utf-8"))
resolution = city["grid"]["h3_resolution"]
pieces = streets.pieces_from_ways(raw["elements"], resolution)
out = ROOT / "build" / "streets" / city["id"] / "streets.json"
out.parent.mkdir(parents=True, exist_ok=True)
payload = {"city": city["id"], "attribution": "© OpenStreetMap contributors (ODbL)", "pieces": pieces}
out.write_text(json.dumps(payload, separators=(",", ":"), ensure_ascii=False), encoding="utf-8")
cells = grid.cells_for_bbox(city["grid"]["bbox"], resolution)
print(json.dumps({"file": str(out.relative_to(ROOT)), "bytes": out.stat().st_size, **streets.summary(pieces, cells)}))
