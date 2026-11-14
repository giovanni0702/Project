"""Queueing model of on-street parking occupancy (city-agnostic, standard library only).

Spaces are servers, parked cars are customers (T-049, docs/09-modello.md "Modello di occupazione").
- Erlang B and C for real-valued c, computed through the regularized incomplete gamma function,
  stable for thousands of spaces.
- Time-varying demand: modified offered load (MOL), i.e. the stock of the infinite-server system
  driven by the time-varying arrival rate, then used as offered load a(t).
- Waiting time: M/M/c formula P(W <= t) = 1 - C(c, a) exp(-(c mu - lambda) t). It has no steady
  state when lambda >= c mu, so the build uses a finite-patience M/M/c/(c+K) queue: a driver who
  finds K or more drivers already searching gives up. Stable for every load; as K grows and
  lambda < c mu it converges to the M/M/c formula (tested).
- Uncertainty: Monte Carlo over declared parameter ranges with a fixed seed.
- Calibration: Bayesian posterior of a per-zone demand scale factor from binary outcomes.
All outputs are MODEL ESTIMATES until calibrated on real outcomes.
"""
import math
import random

_EPS = 1e-15


def _log_gamma_q(s: float, x: float) -> float:
    """log Q(s, x), the regularized upper incomplete gamma function (Numerical Recipes gser / gcf)."""
    if x <= 0:
        return 0.0
    prefactor = -x + s * math.log(x) - math.lgamma(s)
    if x < s + 1:
        term = total = 1.0 / s
        n = s
        for _ in range(100000):
            n += 1
            term *= x / n
            total += term
            if term < total * _EPS:
                break
        lower = math.exp(prefactor) * total
        return math.log1p(-lower) if lower < 1 else -math.inf
    tiny = 1e-300
    b = x + 1 - s
    c, d = 1 / tiny, 1 / b
    h = d
    for i in range(1, 100000):
        an = -i * (i - s)
        b += 2
        d = an * d + b
        d = tiny if abs(d) < tiny else d
        c = b + an / c
        c = tiny if abs(c) < tiny else c
        d = 1 / d
        delta = d * c
        h *= delta
        if abs(delta - 1) < _EPS:
            break
    return prefactor + math.log(h)


def gamma_p(s: float, x: float) -> float:
    """Regularized lower incomplete gamma P(s, x) = P(Gamma(s, 1) <= x)."""
    return -math.expm1(_log_gamma_q(s, x)) if x > 0 else 0.0


def erlang_b(c: float, a: float) -> float:
    """Erlang B blocking probability for c servers (real c >= 0) and offered load a.

    B(c, a) = Poisson pmf(c; a) / Poisson cdf(c; a), with the cdf written as Q(c + 1, a), so that
    non-integer capacities (expected values) are allowed and large c does not overflow.
    """
    if a <= 0:
        return 0.0 if c > 0 else 1.0
    if c <= 0:
        return 1.0
    log_pmf = c * math.log(a) - a - math.lgamma(c + 1)
    return min(1.0, math.exp(log_pmf - _log_gamma_q(c + 1, a)))


def erlang_b_recursive(n: int, a: float) -> float:
    """Classic recursion B(k) = a B(k-1) / (k + a B(k-1)); integer n only. Used as a test reference."""
    b = 1.0
    for k in range(1, n + 1):
        b = a * b / (k + a * b)
    return b


def erlang_c(c: float, a: float) -> float:
    """Erlang C: probability that an arrival waits in M/M/c. Equals 1 when a >= c (no steady state)."""
    if a <= 0:
        return 0.0
    if a >= c:
        return 1.0
    b = erlang_b(c, a)
    return b / (1 - (a / c) * (1 - b))


def mmc_wait_cdf(c: float, lam: float, mu: float, t: float) -> tuple[float, bool]:
    """M/M/c: (P(W <= t), overloaded). P = 1 - C(c, a) exp(-(c mu - lam) t).

    Overload (lam >= c mu): the queue grows without bound, P(W <= t) -> 0 for every finite t, and the
    flag is True. Use finite_patience_queue() to obtain a stable value under overload.
    """
    if lam <= 0:
        return 1.0, False
    if c <= 0 or lam >= c * mu:
        return 0.0, True
    return 1 - erlang_c(c, lam / mu) * math.exp(-(c * mu - lam) * t), False


def finite_patience_queue(c: float, lam: float, mu: float, t: float, patience: float) -> dict:
    """M/M/c/(c+K) with K = ceil(c mu patience): drivers ahead beyond the departures expected within
    the patience time make a newcomer give up (counted as "not found").

    Returns p_found (P(found within t) for a random arriving driver), busy (expected occupied
    spaces), blocked (share giving up on arrival), rho = lam / (c mu), overloaded = rho >= 1.
    Stationary probabilities: pi_n ~ a^n/n! for n <= c, pi_(c+j) = pi_c rho^j for j <= K.
    An admitted driver finding j drivers ahead waits Gamma(j + 1, c mu).
    """
    if c <= 0:
        return {"p_found": 0.0, "busy": 0.0, "blocked": 1.0, "rho": math.inf, "overloaded": True}
    if lam <= 0 or mu <= 0:
        return {"p_found": 1.0, "busy": 0.0, "blocked": 0.0, "rho": 0.0, "overloaded": False}
    a = lam / mu
    rho = a / c
    b = erlang_b(c, a)
    if b < 1e-13:
        return {"p_found": 1.0 - b, "busy": a * (1 - b), "blocked": 0.0, "rho": rho, "overloaded": False}
    k = max(1, math.ceil(c * mu * patience))
    log_rho = math.log(rho)
    shift = max(0.0, k * log_rho)  # rescales rho^j to avoid overflow under overload
    x = c * mu * t
    log_x = math.log(x) if x > 0 else -math.inf
    weighted_found = weights = 0.0
    cumulative = 0.0
    for j in range(k + 1):
        exponent = j * log_rho - shift
        if log_rho < 0 and exponent < -40:
            break
        w = math.exp(exponent)
        if j >= 1:
            weights += w
        if j < k:
            cumulative += math.exp(j * log_x - x - math.lgamma(j + 1)) if x > 0 else (1.0 if j == 0 else 0.0)
            weighted_found += w * max(0.0, 1.0 - cumulative)
    base = math.exp(-shift)
    z = base + b * weights
    p_found = ((1 - b) * base + b * weighted_found) / z
    busy = (a * (1 - b) * base + c * b * weights) / z
    blocked = b * math.exp(k * log_rho - shift) / z
    return {"p_found": min(1.0, max(0.0, p_found)), "busy": min(c, busy), "blocked": blocked,
            "rho": rho, "overloaded": rho >= 1}


def mol_stock(arrivals: list[float], mean_dwell: float, slot_minutes: float, days: int = 6) -> list[float]:
    """Modified offered load: expected stock of an infinite-server system with exponential dwell.

    arrivals: expected arrivals in each slot of a periodic day. Returns the stock at each slot's
    midpoint in the periodic regime (the same day repeated `days` times from empty).
    Exact for piecewise-constant rates: m' = m e^(-mu d) + (lambda / mu)(1 - e^(-mu d)).
    """
    mu = 1.0 / mean_dwell
    full, half = math.exp(-mu * slot_minutes), math.exp(-mu * slot_minutes / 2)
    stock, mid = 0.0, [0.0] * len(arrivals)
    for _ in range(days):
        for i, n in enumerate(arrivals):
            level = n / slot_minutes / mu
            mid[i] = stock * half + level * (1 - half)
            stock = stock * full + level * (1 - full)
    return mid


def slot_state(capacity: float, stock: float, arrival_rate: float, t: float, patience: float) -> dict:
    """State of one zone in one slot. stock = offered load a(t) (cars wanting to be parked),
    arrival_rate = cars per minute looking for a space. Service rate mu = arrival_rate / stock
    (Little's law). Returns occupied, free, p_found, overloaded."""
    if stock <= 0 or arrival_rate <= 0:
        occupied = min(capacity, max(stock, 0.0))
        return {"occupied": occupied, "free": capacity - occupied, "p_found": 1.0 if capacity - occupied >= 1 else 0.0,
                "overloaded": stock >= capacity}
    q = finite_patience_queue(capacity, arrival_rate, arrival_rate / stock, t, patience)
    return {"occupied": q["busy"], "free": capacity - q["busy"], "p_found": q["p_found"], "overloaded": q["overloaded"]}


def sample_parameters(spec: dict, draws: int, seed: int) -> list[dict]:
    """Draw 0 is the central value; the others are triangular(min, max, mode=central) with a fixed seed.

    spec: {name: [central, min, max]} or {name: number} (fixed) or nested dicts of these.
    """
    rng = random.Random(seed)

    def draw(value, central):
        if isinstance(value, dict):
            return {k: draw(v, central) for k, v in sorted(value.items())}
        if isinstance(value, (list, tuple)) and len(value) == 3 and all(isinstance(v, (int, float)) for v in value):
            mid, low, high = value
            return float(mid) if central or low == high else rng.triangular(low, high, mid)
        return value

    return [draw(spec, True)] + [draw(spec, False) for _ in range(draws)]


def percentile(values: list[float], pct: float) -> float:
    """Linear-interpolation percentile (pct in 0..100)."""
    ordered = sorted(values)
    if not ordered:
        return math.nan
    position = (len(ordered) - 1) * pct / 100
    low = math.floor(position)
    high = min(low + 1, len(ordered) - 1)
    return ordered[low] + (ordered[high] - ordered[low]) * (position - low)


def scaled_found_probability(features: tuple, scale: float) -> float:
    """Default predictor for calibration: features = (capacity, stock, arrival_rate, t, patience);
    the demand scale multiplies stock and arrival rate together (dwell unchanged)."""
    capacity, stock, rate, t, patience = features
    return slot_state(capacity, stock * scale, rate * scale, t, patience)["p_found"]


def calibrate_demand_scale(observations: list[tuple], predict=scaled_found_probability, prior_sd: float = 0.5,
                           log_range: float = 2.0, steps: int = 401, interval: float = 0.9) -> dict:
    """Posterior of a demand scale factor s for one zone from binary outcomes ("found within t").

    observations: [(features, found_bool)]. Prior: log s ~ Normal(0, prior_sd). Likelihood:
    Bernoulli(predict(features, s)). Posterior computed on a grid of log s in [-log_range, log_range].
    Returns scale (posterior mean), map, low, high (central interval), n.
    """
    grid = [-log_range + 2 * log_range * i / (steps - 1) for i in range(steps)]
    log_post = []
    for g in grid:
        s = math.exp(g)
        total = -0.5 * (g / prior_sd) ** 2
        for features, found in observations:
            p = min(1 - 1e-9, max(1e-9, predict(features, s)))
            total += math.log(p if found else 1 - p)
        log_post.append(total)
    top = max(log_post)
    weights = [math.exp(v - top) for v in log_post]
    norm = sum(weights)
    weights = [w / norm for w in weights]
    cumulative, low, high = 0.0, grid[0], grid[-1]
    tail = (1 - interval) / 2
    found_low = False
    for g, w in zip(grid, weights):
        cumulative += w
        if not found_low and cumulative >= tail:
            low, found_low = g, True
        if cumulative >= 1 - tail:
            high = g
            break
    best = grid[weights.index(max(weights))]
    return {"scale": sum(math.exp(g) * w for g, w in zip(grid, weights)), "map": math.exp(best),
            "low": math.exp(low), "high": math.exp(high), "n": len(observations)}
