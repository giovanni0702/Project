"""Probability that a parking search succeeds within the target time.

Model ladder (docs/09-modello.md): baseline frequency, then Beta-Binomial with
time decay, per-contributor weight cap and spatial shrinkage. Outcomes are
binary: found within the target time, or not.
"""
from collections import defaultdict
from dataclasses import dataclass


@dataclass(frozen=True)
class Outcome:
    cell: str
    slot: tuple[str, int]
    success: bool
    age_days: float
    contributor: str  # rotating pseudonymous id, never a stable identity


@dataclass(frozen=True)
class Estimate:
    probability: float
    reliability: str          # "high" | "medium" | "low"
    level: str                # "high" | "mid" | "low" | "unknown"
    n_outcomes: int
    n_contributors: int
    from_user_data: bool      # False when only the prior is published (below k)


def decay_weight(age_days: float, half_life_days: float) -> float:
    return 0.5 ** (age_days / half_life_days)


def baseline(outcomes: list[Outcome]) -> dict[tuple, float]:
    """Mandatory baseline: raw success frequency per (cell, slot)."""
    hits, totals = defaultdict(int), defaultdict(int)
    for o in outcomes:
        totals[(o.cell, o.slot)] += 1
        hits[(o.cell, o.slot)] += o.success
    return {key: hits[key] / totals[key] for key in totals}


def _weighted_counts(outcomes: list[Outcome], params: dict) -> dict[tuple, dict]:
    per_contributor = defaultdict(float)
    stats = defaultdict(lambda: {"s": 0.0, "f": 0.0, "n": 0, "ids": set(), "min_age": float("inf")})
    for o in sorted(outcomes, key=lambda x: x.age_days):  # newest first keep their weight
        key = (o.cell, o.slot)
        weight = decay_weight(o.age_days, params["half_life_days"])
        room = params["max_weight_per_contributor"] - per_contributor[(key, o.contributor)]
        weight = max(0.0, min(weight, room))
        per_contributor[(key, o.contributor)] += weight
        entry = stats[key]
        entry["s" if o.success else "f"] += weight
        entry["n"] += 1
        entry["ids"].add(o.contributor)
        entry["min_age"] = min(entry["min_age"], o.age_days)
    return stats


def _reliability(n: int, min_age: float, rules: dict) -> str:
    for name in ("high", "medium"):
        rule = rules[name]
        if n >= rule["min_outcomes"] and min_age <= rule["max_age_days"]:
            return name
    return "low"


def _level(p: float, thresholds: dict, hysteresis: float, previous: str | None) -> str:
    high, low = thresholds["high"], thresholds["low"]
    if previous == "high" and p >= high - hysteresis:
        return "high"
    if previous == "low" and p <= low + hysteresis:
        return "low"
    if previous == "mid" and low - hysteresis < p < high + hysteresis:
        return "mid"
    return "high" if p >= high else "low" if p <= low else "mid"


def estimate(
    cells: list[str],
    slot: tuple[str, int],
    outcomes: list[Outcome],
    config: dict,
    neighbors_of,
    prior_mean: dict[str, float] | None = None,
    previous_levels: dict[str, str] | None = None,
) -> dict[str, Estimate]:
    """Estimate every cell for one slot. Cells below k publish the prior only."""
    params, display = config["model"], config["display"]
    k = config["privacy"]["min_contributors"]
    strength = params["prior_strength"]
    prior_mean = prior_mean or {}
    previous_levels = previous_levels or {}
    stats = _weighted_counts([o for o in outcomes if o.slot == slot], params)

    def publishable(cell):
        entry = stats.get((cell, slot))
        return entry if entry and len(entry["ids"]) >= k else None

    result = {}
    for cell in cells:
        mean = prior_mean.get(cell, params["prior_mean_default"])
        alpha, beta = mean * strength, (1 - mean) * strength
        # Spatial shrinkage: borrow a fraction of publishable neighbours' evidence.
        for other in neighbors_of(cell):
            entry = publishable(other)
            if entry:
                alpha += params["neighbor_weight"] * entry["s"]
                beta += params["neighbor_weight"] * entry["f"]
        own = publishable(cell)
        if own:
            alpha += own["s"]
            beta += own["f"]
        p = alpha / (alpha + beta)
        n = own["n"] if own else 0
        reliability = _reliability(n, own["min_age"], display["reliability"]) if own else "low"
        result[cell] = Estimate(
            probability=p,
            reliability=reliability,
            level=_level(p, display["thresholds"], display["hysteresis"], previous_levels.get(cell)),
            n_outcomes=n,
            n_contributors=len(own["ids"]) if own else 0,
            from_user_data=bool(own),
        )
    return result
