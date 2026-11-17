"""T-050: structure of the occupancy build (resident vehicles, zone table, plausibility checks).
Synthetic inputs: these tests check the code, NOT the accuracy of the model."""
import pathlib
import sys

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "scripts"))
import build_occupancy as b  # noqa: E402

RULES = {"reference_zones": [1, 2, 3], "centre_zones": [1], "dense_residential_zones": [2], "periphery_zones": [3],
         "day_hour": 11, "city_night_occupancy": [0.6, 1.0], "dense_night_occupancy": [0.85, 1.0],
         "centre_day_p_found": [0.0, 0.6], "min_centre_periphery_gap": 0.2}


def test_resident_vehicles_adds_unregistered_cars_and_goods_vehicles():
    ctx = {"residents": {"a": 1000.0}, "cars_per_resident": 0.5, "goods_per_resident": 0.04}
    base = {"on_street_share": 0.4}
    assert b.resident_vehicles(ctx, "a", base) == pytest.approx(200.0)  # old behaviour without new parameters
    full = {**base, "unregistered_car_factor": 1.1, "goods_on_street_share": 0.5}
    assert b.resident_vehicles(ctx, "a", full) == pytest.approx(1000 * (0.5 * 1.1 * 0.4 + 0.04 * 0.5))
    assert b.resident_vehicles(ctx, "missing", full) == 0.0


def _entry(cap, occ, p, slots=48):
    return {"cap": [cap, cap, cap], "weekday": {"occ": [[occ] * slots], "p": [[p] * slots]}}


def test_zone_table_weights_by_capacity():
    ctx = {"slot_minutes": 30, "cell_zone": {"x": 1, "y": 1, "z": 9}, "zone_names": {1: "Centre"}}
    per_cell = {"x": _entry(100, 90, 20), "y": _entry(300, 300, 60), "z": _entry(50, 0, 100)}
    row = b.zone_table(ctx, per_cell, [1], [3, 11])[1]
    assert row["capacity"] == 400 and row["occupancy"][11] == pytest.approx(0.975, abs=0.006)
    assert row["p_found_pct"][11] == 50  # (20*100 + 60*300) / 400


def _totals(night_occ):
    slots = 48
    day = {"occ": [[0, night_occ, 0]] * slots, "visitors": [[0, 50, 0]] * slots, "away": [[0, 100, 0]] * slots}
    return {"capacity": [0, 1000, 0], "weekday": day}


def _table(centre_p, periphery_p, dense_occ):
    return {1: {"capacity": 100, "occupancy": {3: 0.9}, "p_found_pct": {11: centre_p}},
            2: {"capacity": 100, "occupancy": {3: dense_occ}, "p_found_pct": {11: 30}},
            3: {"capacity": 100, "occupancy": {3: 0.5}, "p_found_pct": {11: periphery_p}}}


def test_plausibility_checks_pass_on_plausible_synthetic_case():
    checks = b.plausibility_checks(_totals(700), _table(40, 95, 0.95), 1500, RULES, 30)
    assert all(c["ok"] for c in checks), checks


def test_plausibility_checks_flag_easy_centre_and_empty_nights():
    checks = {c["name"]: c["ok"] for c in b.plausibility_checks(_totals(500), _table(95, 95, 0.7), 1500, RULES, 30)}
    assert not checks["weekday 03:00 occupied / capacity (city)"]
    assert not checks["weekday 03:00 occupancy, dense residential zones"]
    assert not checks["weekday 11:00 P(found), centre zones"]
    assert not checks["weekday 11:00 P(found), centre minus periphery"]
