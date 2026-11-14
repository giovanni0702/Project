#!/usr/bin/env python3
"""Build the self-contained web app (desktop and phone browsers) for a city.
Usage: scripts/build_webapp.py <city_id>  ->  build/webapp/<city_id>.html
Needs build/streets and build/parking (scripts/build_streets.py, scripts/build_parking.py)."""
import importlib
import json
import pathlib
import sys

import h3

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from parking_core.config import load_city  # noqa: E402

Q = 40000  # quantisation steps across the bounding box (about half a metre)
city = load_city(sys.argv[1])
adapter = importlib.import_module(f"cities.{city['id']}.adapter")
pieces = json.loads((ROOT / "build" / "streets" / city["id"] / "streets.json").read_text(encoding="utf-8"))["pieces"]
parking = json.loads((ROOT / "build" / "parking" / city["id"] / "parking.json").read_text(encoding="utf-8"))

lons = [pt[0] for p in pieces for pt in p["line"]]
lats = [pt[1] for p in pieces for pt in p["line"]]
west, east, south, north = min(lons), max(lons), min(lats), max(lats)


def qx(lon): return round((lon - west) / (east - west) * Q)
def qy(lat): return round((lat - south) / (north - south) * Q)


def encode(points, head=()):
    row, px, py = list(head), 0, 0
    for lon, lat in points:
        x, y = qx(lon), qy(lat)
        if len(row) > len(head) and x == px and y == py:
            continue
        row += [x - px, y - py]
        px, py = x, y
    return row


names, name_index, cells, cell_index, out, stalls = [], {}, [], {}, [], []
for number, piece in enumerate(pieces):
    if piece["cell"] not in cell_index:
        lat, lon = h3.cell_to_latlng(piece["cell"])
        cell_index[piece["cell"]] = len(cells)
        cells.append([qx(lon), qy(lat)])
    if piece["name"] not in name_index:
        name_index[piece["name"]] = len(names)
        names.append(piece["name"])
    row = encode(piece["line"], (cell_index[piece["cell"]], name_index[piece["name"]]))
    if len(row) >= 6:
        out.append(row)
        stalls.append(parking["per_piece"].get(str(number), 0))

layers = {"green": [], "water": [], "building": [], "parking": [], "rail": []}
for shape in adapter.basemap():
    row = encode(shape["points"])
    if len(row) >= (6 if shape["kind"] == "polygon" else 4):
        layers[shape["layer"]].append(row)

KIND_LABEL = {"garage": "Autorimessa convenzionata", "public": "Parcheggio pubblico",
              "public_residents": "Parcheggio pubblico e residenti", "park_and_ride": "Parcheggio di interscambio"}
car_parks = [[qx(c["lon"]), qy(c["lat"]), c["name"], KIND_LABEL[c["kind"]], c["spaces"], c.get("address", ""), c.get("note", "")]
             for c in parking["car_parks"]]
center = [sum(c[0] for c in cells) / len(cells), sum(c[1] for c in cells) / len(cells)]
data = {"city": city["name"], "bbox": [west, south, east, north], "q": Q, "names": names, "cells": cells, "pieces": out,
        "stalls": stalls, "carParks": car_parks, "layers": layers, "odds": city["vehicles"]["odds"],
        "thresholds": city["display"]["thresholds"], "center": center, "attribution": adapter.ATTRIBUTION}
html = (ROOT / "web" / "app_template.html").read_text(encoding="utf-8")
html = html.replace("/*DATA*/null", json.dumps(data, separators=(",", ":"), ensure_ascii=False))
target = ROOT / "build" / "webapp" / f"{city['id']}.html"
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(html, encoding="utf-8")
print(f"{target.relative_to(ROOT)} {target.stat().st_size} bytes; pieces {len(out)}; " + ", ".join(f"{k} {len(v)}" for k, v in layers.items()))
