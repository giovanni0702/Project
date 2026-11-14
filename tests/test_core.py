"""Technical tests on SYNTHETIC data. They verify the code, not model accuracy."""
import random
import re
from datetime import datetime
from pathlib import Path

from parking_core import grid, metrics, slots
from parking_core.config import load_city
from parking_core.model import Outcome, baseline, estimate

CITY = load_city("milano")
SLOT = ("weekday", 37)
CELLS = grid.cells_for_bbox(CITY["grid"]["bbox"], CITY["grid"]["h3_resolution"])


def synthetic(cell, successes, failures, contributors, age=1.0):
    flags = [True] * successes + [False] * failures
    return [Outcome(cell, SLOT, f, age, f"c{i % contributors}") for i, f in enumerate(flags)]


def run(outcomes, **kwargs):
    return estimate(CELLS, SLOT, outcomes, CITY, grid.neighbors, **kwargs)


def test_core_has_no_city_specific_values():
    forbidden = re.compile(r"milan|europe/rome|45\.\d|9\.[01]\d", re.I)
    for path in Path("parking_core").glob("*.py"):
        assert not forbidden.search(path.read_text()), path


def test_grid_covers_city_and_is_global():
    assert 1000 < len(CELLS) < 5000
    assert grid.to_cell(45.4642, 9.19, CITY["grid"]["h3_resolution"]) in CELLS
    assert len(grid.neighbors(CELLS[0])) == 6


def test_slots():
    key = slots.slot_key(datetime(2026, 11, 16, 18, 45), CITY["time"]["slot_minutes"])
    assert key == SLOT
    assert slots.day_type(datetime(2026, 11, 15).date()) == "holiday"


def test_no_data_publishes_prior_with_low_reliability():
    est = run([])[CELLS[0]]
    assert est.probability == CITY["model"]["prior_mean_default"]
    assert est.reliability == "low" and not est.from_user_data


def test_below_k_contributors_only_prior_is_published():
    cell = CELLS[10]
    est = run(synthetic(cell, 40, 0, contributors=4))[cell]
    assert not est.from_user_data and est.n_outcomes == 0
    assert est.probability == CITY["model"]["prior_mean_default"]


def test_below_k_does_not_leak_into_neighbours():
    cell = CELLS[10]
    result = run(synthetic(cell, 40, 0, contributors=4))
    assert all(result[n].probability == CITY["model"]["prior_mean_default"] for n in grid.neighbors(cell) if n in result)


def test_enough_data_moves_estimate_and_neighbours():
    cell = CELLS[10]
    result = run(synthetic(cell, 36, 4, contributors=12))
    est = result[cell]
    assert est.from_user_data and est.probability > 0.75 and est.level == "high"
    assert est.reliability == "high"
    neighbour = next(n for n in grid.neighbors(cell) if n in result)
    assert 0.5 < result[neighbour].probability < est.probability


def test_single_contributor_cannot_dominate():
    cell = CELLS[10]
    honest = synthetic(cell, 5, 5, contributors=10)
    spam = [Outcome(cell, SLOT, True, 0.1, "spammer") for _ in range(200)]
    assert run(honest + spam)[cell].probability < 0.7


def test_old_outcomes_fade():
    cell = CELLS[10]
    fresh = run(synthetic(cell, 30, 0, contributors=10, age=1))[cell]
    stale = run(synthetic(cell, 30, 0, contributors=10, age=200))[cell]
    assert stale.probability < fresh.probability
    assert stale.reliability == "low"


def test_hysteresis_keeps_level_near_threshold():
    cell = CELLS[10]
    outcomes = synthetic(cell, 19, 11, contributors=10)  # just below the "high" threshold
    assert run(outcomes)[cell].level == "mid"
    assert run(outcomes, previous_levels={cell: "high"})[cell].level == "high"


def test_metrics_on_synthetic_data():
    rng = random.Random(7)
    truth = [rng.random() for _ in range(5000)]
    seen = [rng.random() < p for p in truth]
    assert metrics.calibration_error(truth, seen) < 0.03
    assert metrics.calibration_error([min(1, p + 0.3) for p in truth], seen) > 0.15
    constant = [sum(seen) / len(seen)] * len(seen)
    assert metrics.skill_vs_baseline(metrics.brier(truth, seen), metrics.brier(constant, seen)) > 0.2


def test_baseline_frequency():
    cell = CELLS[10]
    assert baseline(synthetic(cell, 3, 1, contributors=4))[(cell, SLOT)] == 0.75


def test_search_time_becomes_binary_target():
    from parking_core.model import success_from_search
    target = CITY["model"]["target_minutes"]
    assert success_from_search(3.5, target) and not success_from_search(9, target)


def test_live_outcomes_move_the_estimate_now():
    cell = CELLS[10]
    history = synthetic(cell, 30, 10, contributors=10, age=5)
    other_slot = (SLOT[0], SLOT[1] - 1)
    live = [Outcome(cell, other_slot, False, 20 / 1440, f"live{i}") for i in range(8)]
    before, after = run(history)[cell], run(history + live)[cell]
    assert before.probability > 0.7
    assert after.probability < before.probability - 0.15


def test_published_grid_has_aggregates_only():
    import json
    from parking_core.publish import build_grid
    payload = build_grid(CITY, outcomes=synthetic(CELLS[10], 36, 4, contributors=12))
    text = json.dumps(payload)
    assert payload["valid_minutes"] == 5 and len(payload["cells"]) == len(CELLS)
    assert "c1" not in json.dumps(list(payload["cells"].values())) and "contributor" not in text
    assert payload["cells"][CELLS[10]][3] is True
