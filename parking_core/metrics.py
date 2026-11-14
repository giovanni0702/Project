"""Calibration metrics. Reports on synthetic data are technical tests only,
never a measure of accuracy (docs/09-modello.md)."""
import math
import random
from collections import defaultdict


def brier(probabilities: list[float], outcomes: list[bool]) -> float:
    return sum((p - o) ** 2 for p, o in zip(probabilities, outcomes)) / len(outcomes)


def skill_vs_baseline(model_brier: float, baseline_brier: float) -> float:
    """Positive = better than baseline. 0.1 means 10% lower Brier score."""
    return 1 - model_brier / baseline_brier


def reliability_table(probabilities: list[float], outcomes: list[bool], bins: int = 10) -> list[dict]:
    rows = [{"n": 0, "p_sum": 0.0, "hits": 0} for _ in range(bins)]
    for p, o in zip(probabilities, outcomes):
        row = rows[min(int(p * bins), bins - 1)]
        row["n"] += 1
        row["p_sum"] += p
        row["hits"] += o
    return [
        {"bin": i, "n": r["n"], "predicted": r["p_sum"] / r["n"], "observed": r["hits"] / r["n"]}
        for i, r in enumerate(rows) if r["n"]
    ]


def calibration_error(probabilities: list[float], outcomes: list[bool], bins: int = 10) -> float:
    """Expected calibration error: mean |predicted - observed| weighted by bin size."""
    table = reliability_table(probabilities, outcomes, bins)
    total = sum(r["n"] for r in table)
    return sum(r["n"] * abs(r["predicted"] - r["observed"]) for r in table) / total


def min_outcomes_per_bin(tolerance: float = 0.10, z: float = 1.96, p: float = 0.5) -> int:
    """Outcomes a bin needs so that the 95% half-width of its observed frequency
    is within `tolerance` (worst case p = 0.5): 97 for the proposed ±10 points."""
    return math.ceil(z * z * p * (1 - p) / (tolerance * tolerance))


def enough_data(n: int, n_groups: int | None = None, bins: int = 3, tolerance: float = 0.10,
                min_groups: int = 10) -> bool:
    """True when a calibration claim is allowed at all.

    `bins` defaults to the 3 published classes (low / mid / high): each needs
    min_outcomes_per_bin(tolerance) outcomes, so about 300 in total. `n_groups`
    is the number of distinct contributors: outcomes of one person are correlated,
    so with fewer than `min_groups` the interval is not trusted either.
    Below this nothing is declared, not even with a confidence interval.
    """
    if n < bins * min_outcomes_per_bin(tolerance):
        return False
    return n_groups is None or n_groups >= min_groups


def bootstrap_ci(metric, probabilities: list[float], outcomes: list[bool], groups: list | None = None,
                 n_boot: int = 1000, level: float = 0.95, seed: int = 0) -> tuple[float, float, float]:
    """(point, low, high) percentile interval of `metric(probabilities, outcomes)`.

    With `groups` (e.g. contributor or cell) whole groups are resampled: outcomes
    of the same person are not independent, and resampling them one by one would
    give intervals that are too narrow.
    """
    if not outcomes:
        raise ValueError("no outcomes")
    rng = random.Random(seed)
    clusters = defaultdict(list)
    for i, g in enumerate(groups if groups is not None else range(len(outcomes))):
        clusters[g].append(i)
    members = list(clusters.values())
    stats = []
    for _ in range(n_boot):
        idx = [i for _ in members for i in rng.choice(members)]
        stats.append(metric([probabilities[i] for i in idx], [outcomes[i] for i in idx]))
    stats.sort()
    tail = (1 - level) / 2
    low = stats[int(tail * (n_boot - 1))]
    high = stats[int(math.ceil((1 - tail) * (n_boot - 1)))]
    return metric(probabilities, outcomes), low, high


def brier_ci(probabilities, outcomes, groups=None, **kwargs) -> tuple[float, float, float]:
    return bootstrap_ci(brier, probabilities, outcomes, groups, **kwargs)


def calibration_error_ci(probabilities, outcomes, groups=None, bins: int = 10,
                         **kwargs) -> tuple[float, float, float]:
    return bootstrap_ci(lambda p, o: calibration_error(p, o, bins), probabilities, outcomes, groups, **kwargs)


def temporal_split(items: list, time_of, validation_share: float = 0.25, gap: float = 0.0) -> tuple[list, list]:
    """Train on the past, validate on the future; never a random split.

    `time_of(item)` grows with recency. Validation = items at or after the cutoff
    that leaves `validation_share` of items in the future (ties stay together);
    items in the `gap` before the cutoff are dropped so recent-evidence weighting
    cannot leak across the boundary.
    """
    if not 0 < validation_share < 1:
        raise ValueError("validation_share must be in (0, 1)")
    if not items:
        return [], []
    times = sorted(time_of(x) for x in items)
    cutoff = times[min(len(times) - 1, int(len(times) * (1 - validation_share)))]
    train = [x for x in items if time_of(x) < cutoff - gap]
    validation = [x for x in items if time_of(x) >= cutoff]
    return train, validation
