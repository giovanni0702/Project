"""H3 grid helpers. H3 is global, so the same code serves any city."""
import h3


def cells_for_bbox(bbox: dict, resolution: int) -> list[str]:
    ring = [
        (bbox["south"], bbox["west"]),
        (bbox["south"], bbox["east"]),
        (bbox["north"], bbox["east"]),
        (bbox["north"], bbox["west"]),
    ]
    return sorted(h3.polygon_to_cells(h3.LatLngPoly(ring), resolution))


def neighbors(cell: str) -> list[str]:
    return [c for c in h3.grid_disk(cell, 1) if c != cell]


def to_cell(lat: float, lng: float, resolution: int) -> str:
    """On-device reduction mirrors this: coordinates never reach the server."""
    return h3.latlng_to_cell(lat, lng, resolution)
