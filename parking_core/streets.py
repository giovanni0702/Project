"""Turn OpenStreetMap ways into street pieces, each tied to one grid cell (D-021).

The map colours streets, but estimates and contributions stay per cell:
a piece inherits its cell's estimate. Data (c) OpenStreetMap contributors, ODbL.
"""
from . import grid

PARKING_PREFIXES = ("parking:", "maxstay", "restriction")


def _parking_tags(tags: dict) -> dict:
    return {k: v for k, v in tags.items() if k.startswith(PARKING_PREFIXES)}


def pieces_from_ways(elements: list[dict], resolution: int) -> list[dict]:
    """Split every way where it crosses into another cell."""
    pieces = []
    for way in elements:
        if way.get("type") != "way" or len(way.get("geometry", [])) < 2:
            continue
        tags = way.get("tags", {})
        points = [(p["lat"], p["lon"]) for p in way["geometry"]]
        cells = [grid.to_cell(lat, lon, resolution) for lat, lon in points]
        start = 0
        for i in range(1, len(points) + 1):
            if i == len(points) or cells[i] != cells[start]:
                end = min(i, len(points) - 1)  # include the vertex that crosses over
                if end > start:
                    pieces.append({
                        "way": way["id"],
                        "name": tags.get("name", ""),
                        "kind": tags.get("highway", ""),
                        "cell": cells[start],
                        "line": [[round(lon, 5), round(lat, 5)] for lat, lon in points[start:end + 1]],
                        "parking": _parking_tags(tags),
                    })
                start = i
    return pieces


def summary(pieces: list[dict], cells: list[str]) -> dict:
    covered = {p["cell"] for p in pieces}
    tagged = sum(1 for p in pieces if p["parking"])
    return {
        "pieces": len(pieces),
        "ways": len({p["way"] for p in pieces}),
        "cells_with_streets": round(len(covered & set(cells)) / len(cells), 3),
        "pieces_with_parking_tags": round(tagged / len(pieces), 3) if pieces else 0.0,
    }
