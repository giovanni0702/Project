#!/usr/bin/env python3
"""Build a self-contained preview page of a city's real streets (internal tool).
Usage: scripts/build_preview.py <city_id>  ->  build/preview/<city_id>.html
Needs build/streets/<city_id>/streets.json (scripts/build_streets.py)."""
import importlib
import json
import pathlib
import sys

import h3

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from parking_core.config import load_city  # noqa: E402

Q = 20000  # quantisation steps across the bounding box (about 1 m in a city)
city = load_city(sys.argv[1])
adapter = importlib.import_module(f"cities.{city['id']}.adapter")
pieces = json.loads((ROOT / "build" / "streets" / city["id"] / "streets.json").read_text(encoding="utf-8"))["pieces"]

lons = [pt[0] for p in pieces for pt in p["line"]]
lats = [pt[1] for p in pieces for pt in p["line"]]
west, east, south, north = min(lons), max(lons), min(lats), max(lats)


def qx(lon): return round((lon - west) / (east - west) * Q)
def qy(lat): return round((lat - south) / (north - south) * Q)


parking_file = ROOT / "build" / "parking" / city["id"] / "parking.json"
per_piece = json.loads(parking_file.read_text(encoding="utf-8"))["per_piece"] if parking_file.exists() else {}
names, name_index, cells, cell_index, out, stalls = [], {}, [], {}, [], []
for number, piece in enumerate(pieces):
    if piece["cell"] not in cell_index:
        lat, lon = h3.cell_to_latlng(piece["cell"])
        cell_index[piece["cell"]] = len(cells)
        cells.append([qx(lon), qy(lat)])
    if piece["name"] not in name_index:
        name_index[piece["name"]] = len(names)
        names.append(piece["name"])
    row, px, py = [cell_index[piece["cell"]], name_index[piece["name"]]], 0, 0
    for lon, lat in piece["line"]:
        x, y = qx(lon), qy(lat)
        if len(row) > 2 and x == px and y == py:
            continue
        row += [x - px, y - py]
        px, py = x, y
    if len(row) >= 6:
        out.append(row)
        stalls.append(per_piece.get(str(number), 0))

center = [sum(c[0] for c in cells) / len(cells), sum(c[1] for c in cells) / len(cells)]
data = {"bbox": [west, south, east, north], "q": Q, "names": names, "cells": cells, "pieces": out, "stalls": stalls,
        "odds": city["vehicles"]["odds"], "thresholds": city["display"]["thresholds"], "center": center}
html = (ROOT / "web" / "preview_template.html").read_text(encoding="utf-8")
html = html.replace("/*DATA*/null", json.dumps(data, separators=(",", ":"), ensure_ascii=False))
html = html.replace("__CITY_NAME__", city["name"]).replace("__ATTRIBUTION__", adapter.ATTRIBUTION)
target = ROOT / "build" / "preview" / f"{city['id']}.html"
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(html, encoding="utf-8")
print(f"{target.relative_to(ROOT)} {target.stat().st_size} bytes, {len(out)} pieces, {len(cells)} cells")
