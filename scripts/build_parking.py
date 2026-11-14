#!/usr/bin/env python3
"""Estimate parking capacity per street piece and per cell from mapped parking areas.
Usage: scripts/build_parking.py <city_id>  ->  build/parking/<city_id>/parking.json
Needs build/streets/<city_id>/streets.json. Output is an ESTIMATE from geometry."""
import collections
import importlib
import json
import math
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from parking_core import capacity, grid  # noqa: E402
from parking_core.config import load_city  # noqa: E402

city = load_city(sys.argv[1])
adapter = importlib.import_module(f"cities.{city['id']}.adapter")
resolution = city["grid"]["h3_resolution"]
pieces = json.loads((ROOT / "build" / "streets" / city["id"] / "streets.json").read_text(encoding="utf-8"))["pieces"]
by_cell = collections.defaultdict(list)
for index, piece in enumerate(pieces):
    by_cell[piece["cell"]].append(index)

per_piece, per_cell, kinds, areas = collections.Counter(), collections.Counter(), collections.Counter(), []
unassigned = 0
for area in adapter.parking_areas():
    size, perimeter = capacity.area_and_perimeter(area["ring_m"])
    stalls, kind = capacity.estimate_stalls(size, perimeter)
    if not stalls:
        continue
    lat, lon = area["centroid"]
    cell = grid.to_cell(lat, lon, resolution)
    scale = math.cos(math.radians(lat))
    best, best_d = None, 1e9
    for candidate_cell in [cell, *grid.neighbors(cell)]:
        for index in by_cell.get(candidate_cell, ()):
            for plon, plat in pieces[index]["line"]:
                d = ((plon - lon) * scale) ** 2 + (plat - lat) ** 2
                if d < best_d:
                    best, best_d = index, d
    if best is None:
        unassigned += stalls
    else:
        per_piece[best] += stalls
    per_cell[cell] += stalls
    kinds[kind] += stalls
    areas.append([round(lon, 5), round(lat, 5), stalls, kind])

out = ROOT / "build" / "parking" / city["id"] / "parking.json"
out.parent.mkdir(parents=True, exist_ok=True)
payload = {"city": city["id"], "attribution": adapter.ATTRIBUTION, "method": "estimate from mapped parking-area geometry",
           "car_parks": list(adapter.car_parks()),
           "per_piece": {str(k): v for k, v in per_piece.items()}, "per_cell": dict(per_cell), "areas": areas}
out.write_text(json.dumps(payload, separators=(",", ":")), encoding="utf-8")
print(json.dumps({"file": str(out.relative_to(ROOT)), "car_parks": len(payload["car_parks"]),
                  "car_park_spaces": sum(c["spaces"] or 0 for c in payload["car_parks"]), "areas": len(areas), "estimated_spaces": sum(per_cell.values()),
                  "by_kind": dict(kinds), "pieces_with_spaces": len(per_piece), "cells_with_spaces": len(per_cell),
                  "unassigned_spaces": unassigned}))
