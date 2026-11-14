"""Calibration metrics. Reports on synthetic data are technical tests only,
never a measure of accuracy (docs/09-modello.md)."""


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
