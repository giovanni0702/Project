"""Technical tests on SYNTHETIC data: they verify the metric code, never model accuracy."""
import random
import subprocess
import sys
from pathlib import Path

import pytest

from parking_core import metrics
from parking_core.model import Outcome

ROOT = Path(__file__).resolve().parent.parent


def synthetic_calibrated(n, seed=1, contributors=20):
    """SYNTHETIC: outcomes drawn from the stated probabilities."""
    rng = random.Random(seed)
    probs = [rng.choice([0.2, 0.5, 0.8]) for _ in range(n)]
    hits = [rng.random() < p for p in probs]
    groups = [i % contributors for i in range(n)]
    return probs, hits, groups


def test_min_outcomes_per_bin_matches_tolerance():
    assert metrics.min_outcomes_per_bin(0.10) == 97
    assert metrics.min_outcomes_per_bin(0.05) == 385


def test_enough_data_thresholds():
    assert not metrics.enough_data(290)
    assert metrics.enough_data(291)
    assert not metrics.enough_data(1000, n_groups=9)
    assert metrics.enough_data(1000, n_groups=10)


def test_bootstrap_ci_contains_point_and_is_reproducible():
    probs, hits, groups = synthetic_calibrated(400)
    a = metrics.brier_ci(probs, hits, n_boot=300, seed=7)
    b = metrics.brier_ci(probs, hits, n_boot=300, seed=7)
    assert a == b
    point, low, high = a
    assert point == pytest.approx(metrics.brier(probs, hits))
    assert low <= point <= high
    point, low, high = metrics.calibration_error_ci(probs, hits, bins=3, n_boot=300, seed=7)
    assert low <= point <= high


def test_bootstrap_ci_narrows_with_more_data():
    small = metrics.brier_ci(*synthetic_calibrated(100)[:2], n_boot=300)
    large = metrics.brier_ci(*synthetic_calibrated(2000)[:2], n_boot=300)
    assert large[2] - large[1] < small[2] - small[1]


def test_group_bootstrap_is_wider_for_correlated_outcomes():
    """SYNTHETIC: each contributor always succeeds or always fails."""
    rng = random.Random(3)
    probs, hits, groups = [], [], []
    for g in range(10):
        success = rng.random() < 0.5
        for _ in range(40):
            probs.append(0.5)
            hits.append(success)
            groups.append(g)
    naive = metrics.brier_ci(probs, hits, n_boot=500, seed=1)
    grouped = metrics.brier_ci(probs, hits, groups, n_boot=500, seed=1)
    assert grouped[2] - grouped[1] >= naive[2] - naive[1]


def test_bootstrap_rejects_empty():
    with pytest.raises(ValueError):
        metrics.brier_ci([], [])


def test_temporal_split_never_mixes_past_and_future():
    outcomes = [Outcome("c", ("weekday", 1), True, age, f"p{age}") for age in range(28)]
    recency = lambda o: -o.age_days  # noqa: E731 - larger = more recent
    train, validation = metrics.temporal_split(outcomes, recency, validation_share=0.25)
    assert len(validation) == 7 and len(train) == 21
    assert max(recency(o) for o in train) < min(recency(o) for o in validation)
    train_gap, _ = metrics.temporal_split(outcomes, recency, validation_share=0.25, gap=2)
    assert len(train_gap) == 19


def test_temporal_split_keeps_ties_together():
    items = [0, 0, 1, 1, 1, 1, 2, 2]
    train, validation = metrics.temporal_split(items, lambda x: x, validation_share=0.5)
    assert set(train).isdisjoint(validation)
    with pytest.raises(ValueError):
        metrics.temporal_split(items, lambda x: x, validation_share=1.0)


def test_beta_density_script_runs_and_is_reproducible(tmp_path):
    cmd = [sys.executable, str(ROOT / "scripts" / "beta_density.py"), "--testers", "20",
           "--cells", "14", "--resolutions", "8", "--slot-minutes", "180", "--runs", "2"]
    first = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    second = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    assert first == second
    assert first.startswith("SIMULAZIONE SINTETICA")
