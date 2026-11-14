#!/usr/bin/env python3
"""Download a city's streets and parking features from OpenStreetMap (ODbL).

Usage: scripts/fetch_osm.py <city_id>   ->  data/raw/<city_id>/osm_*.json
Raw files stay out of git; rerun to refresh. Attribution: (c) OpenStreetMap contributors.
"""
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from parking_core.config import load_city  # noqa: E402

ENDPOINT = "https://overpass-api.de/api/interpreter"
STREETS = "residential|living_street|unclassified|tertiary|secondary|primary|tertiary_link|secondary_link|primary_link"
QUERIES = {
    "streets": '[out:json][timeout:240];area(id:{area})->.a;way(area.a)[highway~"^({streets})$"];out tags geom qt;',
    "parking": '[out:json][timeout:240];area(id:{area})->.a;(nwr(area.a)[amenity~"^(parking|parking_space|motorcycle_parking)$"];);out tags center qt;',
    "boundary": "[out:json][timeout:120];rel({relation});out geom;",
}

city = load_city(sys.argv[1])
relation = city["sources"]["osm_relation_id"]
out_dir = ROOT / "data" / "raw" / city["id"]
out_dir.mkdir(parents=True, exist_ok=True)
for name, template in QUERIES.items():
    query = template.format(area=3600000000 + relation, relation=relation, streets=STREETS)
    path = out_dir / f"osm_{name}.json"
    subprocess.run(
        ["curl", "-sS", "-m", "300", "-A", "parking-app-pipeline", "--data-urlencode", f"data={query}", "-o", str(path), ENDPOINT],
        check=True,
    )
    print(f"{path.relative_to(ROOT)} {path.stat().st_size} bytes")
