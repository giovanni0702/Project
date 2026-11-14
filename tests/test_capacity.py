"""Geometry-only capacity estimate. Synthetic shapes: checks the code, not real counts."""
from parking_core.capacity import area_and_perimeter, estimate_stalls, strip_width


def rect(w, h):
    return [(0, 0), (w, 0), (w, h), (0, h)]


def test_area_perimeter_and_width():
    area, perimeter = area_and_perimeter(rect(50, 2.2))
    assert round(area, 1) == 110.0 and round(perimeter, 1) == 104.4
    assert round(strip_width(area, perimeter), 1) == 2.2


def test_parallel_strip_one_car_every_five_metres():
    assert estimate_stalls(*area_and_perimeter(rect(50, 2.2))) == (10, "strip_parallel")


def test_angled_strip_fits_more_cars():
    assert estimate_stalls(*area_and_perimeter(rect(50, 5))) == (20, "strip_angled")


def test_car_park_uses_area():
    assert estimate_stalls(*area_and_perimeter(rect(50, 40))) == (80, "lot")


def test_tiny_area_holds_nothing():
    assert estimate_stalls(*area_and_perimeter(rect(2, 2)))[0] == 0
