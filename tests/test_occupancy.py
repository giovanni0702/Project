"""Occupancy queueing model (T-049). Known-value and limit tests check the maths; the calibration test
uses SYNTHETIC labelled outcomes and checks the code only, never accuracy (docs/09-modello.md)."""
import math
import random

import pytest

from parking_core.capacity import kerbside_stalls, moto_stalls, usable_kerb_length
from parking_core.occupancy import (calibrate_demand_scale, erlang_b, erlang_b_recursive, erlang_c,
                                    finite_patience_queue, mmc_wait_cdf, mol_stock, percentile,
                                    sample_parameters, scaled_found_probability, slot_state)


@pytest.mark.parametrize("c, a, expected", [
    (1, 1.0, 0.5), (2, 1.0, 0.2), (10, 5.0, 0.018385),
    # Erlang B traffic tables: load giving 2% (10 lines) and 1% (50 and 100 lines) blocking.
    (10, 5.08, 0.020), (50, 37.90, 0.010), (100, 84.06, 0.010),
])
def test_erlang_b_known_values(c, a, expected):
    assert erlang_b(c, a) == pytest.approx(expected, abs=5e-4)


@pytest.mark.parametrize("c, a", [(5, 3.0), (30, 40.0), (500, 480.0), (2000, 1900.0), (3000, 3600.0)])
def test_erlang_b_matches_recursion_for_large_c(c, a):
    assert erlang_b(c, a) == pytest.approx(erlang_b_recursive(c, a), rel=1e-9)


def test_erlang_c_known_values():
    assert erlang_c(1, 0.5) == pytest.approx(0.5)          # M/M/1: P(wait) = rho
    assert erlang_c(2, 1.0) == pytest.approx(1 / 3)        # M/M/2 closed form
    assert erlang_c(10, 8.0) == pytest.approx(0.4092, abs=5e-4)
    assert erlang_c(10, 10.0) == 1.0


def test_limits_zero_load_and_huge_capacity():
    assert erlang_b(100, 0.0) == 0.0 and erlang_c(100, 0.0) == 0.0
    assert erlang_b(10000, 100.0) < 1e-300 or erlang_b(10000, 100.0) == 0.0
    assert mmc_wait_cdf(100, 0.0, 0.01, 5) == (1.0, False)
    assert slot_state(50, 0.0, 0.0, 5, 10)["p_found"] == 1.0
    assert finite_patience_queue(5000, 10.0, 0.01, 5, 10)["p_found"] == pytest.approx(1.0)


def test_mmc_overload_is_flagged():
    p, overloaded = mmc_wait_cdf(100, 1.2, 0.01, 5)
    assert overloaded and p == 0.0


def test_finite_patience_converges_to_mmc():
    exact, _ = mmc_wait_cdf(100, 0.9, 0.01, 5)
    q = finite_patience_queue(100, 0.9, 0.01, 5, patience=1e5)
    assert q["p_found"] == pytest.approx(exact, rel=1e-9)
    assert q["busy"] == pytest.approx(90.0, rel=1e-9)


def test_overload_is_stable_and_continuous():
    below = finite_patience_queue(100, 0.999, 0.01, 5, 10)
    above = finite_patience_queue(100, 1.001, 0.01, 5, 10)
    assert above["overloaded"] and not below["overloaded"]
    assert abs(below["p_found"] - above["p_found"]) < 0.02
    heavy = finite_patience_queue(100, 3.0, 0.01, 5, 10)
    assert 0.0 <= heavy["p_found"] < above["p_found"] and heavy["busy"] == pytest.approx(100, rel=0.01)
    huge = finite_patience_queue(2000, 300.0, 0.01, 5, 60)   # rho = 15, K = 1200: no overflow
    assert 0.0 <= huge["p_found"] < 0.2 and huge["blocked"] > 0.8


def test_more_capacity_more_probability():
    values = [finite_patience_queue(c, 1.0, 0.01, 5, 10)["p_found"] for c in (60, 80, 100, 120, 160)]
    assert all(x < y for x, y in zip(values, values[1:]))
    free = [slot_state(c, 90.0, 0.9, 5, 10)["free"] for c in (80, 100, 120)]
    assert all(x < y for x, y in zip(free, free[1:]))


def test_more_demand_less_probability():
    values = [scaled_found_probability((100, 90.0, 0.9, 5, 10), s) for s in (0.5, 1.0, 1.2, 2.0)]
    assert all(x > y for x, y in zip(values, values[1:]))


def test_mol_stock_constant_rate_reaches_little():
    stock = mol_stock([30.0] * 48, mean_dwell=90, slot_minutes=30)  # 1 car/min x 90 min
    assert all(s == pytest.approx(90.0, rel=1e-6) for s in stock)


def test_mol_stock_lags_a_pulse():
    arrivals = [0.0] * 48
    arrivals[16] = 100.0
    stock = mol_stock(arrivals, mean_dwell=120, slot_minutes=30)
    assert stock.index(max(stock)) in (16, 17) and stock[20] > stock[30] > 0


def test_monte_carlo_is_reproducible_and_central_first():
    spec = {"x": [1.0, 0.5, 2.0], "fixed": 3, "nested": {"y": [0.2, 0.1, 0.4]}}
    first, second = sample_parameters(spec, 20, 7), sample_parameters(spec, 20, 7)
    assert first == second and first[0] == {"x": 1.0, "fixed": 3, "nested": {"y": 0.2}}
    assert all(0.5 <= d["x"] <= 2.0 for d in first)
    assert percentile([1, 2, 3, 4], 50) == 2.5


def test_kerbside_capacity_formula():
    usable = usable_kerb_length(110.0, 5.0)
    assert usable == 100.0 and usable_kerb_length(8.0, 5.0) == 0.0
    assert kerbside_stalls(usable, 2, 0.5, 5.0) == pytest.approx(20.0)
    assert kerbside_stalls(usable, 2, 0.5, 5.0, moto_share=0.1) == pytest.approx(18.0)
    assert moto_stalls(usable, 2, 0.5, 0.1, 1.0) == pytest.approx(10.0)


def test_calibration_recovers_known_scale_on_synthetic_outcomes():
    """SYNTHETIC: outcomes drawn from the model itself with a known factor 1.5."""
    rng = random.Random(49)
    true_scale, observations = 1.5, []
    for _ in range(600):
        cap = rng.uniform(60, 150)
        stock = cap * rng.uniform(0.4, 0.9)
        features = (cap, stock, stock / rng.uniform(60, 240), 5, 10)
        p = scaled_found_probability(features, true_scale)
        observations.append((features, rng.random() < p))
    fit = calibrate_demand_scale(observations)
    assert fit["low"] <= true_scale <= fit["high"]
    assert fit["scale"] == pytest.approx(true_scale, rel=0.15) and fit["n"] == 600


def test_calibration_without_data_returns_prior():
    fit = calibrate_demand_scale([])
    assert fit["map"] == pytest.approx(1.0) and fit["low"] < 1.0 < fit["high"]
    assert math.isfinite(fit["scale"])
