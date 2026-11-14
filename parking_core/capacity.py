"""Estimate how many parking spaces a mapped parking area holds (city-agnostic).

Inputs are plain geometry in metres. The result is an ESTIMATE from shape alone:
it is not a count of painted stalls and must be labelled as such in the app.
"""
import math

STALL_LENGTH_M = 5.0        # parallel parking: one car per 5 m of kerb
STALL_WIDTH_M = 2.5         # angled or perpendicular: one car per 2.5 m
LOT_AREA_PER_STALL_M2 = 25  # car parks: stall plus its share of aisles
STRIP_MAX_WIDTH_M = 7.0     # wider than this is a car park, not a kerbside strip
ANGLED_MIN_WIDTH_M = 3.6    # strips at least this wide fit angled or perpendicular stalls


def area_and_perimeter(points: list[tuple[float, float]]) -> tuple[float, float]:
    """Shoelace area and perimeter of a ring given in metres."""
    area = perimeter = 0.0
    for (x1, y1), (x2, y2) in zip(points, points[1:] + points[:1]):
        area += x1 * y2 - x2 * y1
        perimeter += math.hypot(x2 - x1, y2 - y1)
    return abs(area) / 2, perimeter


def strip_width(area: float, perimeter: float) -> float:
    """Width of the rectangle with the same area and perimeter (narrow side)."""
    root = perimeter * perimeter - 16 * area
    return (perimeter - math.sqrt(root)) / 4 if root > 0 else math.sqrt(area)


def estimate_stalls(area: float, perimeter: float) -> tuple[int, str]:
    """Return (estimated spaces, kind) with kind in strip_parallel | strip_angled | lot."""
    if area < STALL_LENGTH_M * 1.8:
        return 0, "too_small"
    width = strip_width(area, perimeter)
    if width <= STRIP_MAX_WIDTH_M:
        length = area / max(width, 1.8)
        if width >= ANGLED_MIN_WIDTH_M:
            return int(length / STALL_WIDTH_M), "strip_angled"
        return int(length / STALL_LENGTH_M), "strip_parallel"
    return int(area / LOT_AREA_PER_STALL_M2), "lot"
