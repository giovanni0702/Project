#!/usr/bin/env python3
"""T-029: how many cell-slots reach k distinct contributors during a small beta?

SYNTHETIC SIMULATION: it sizes the beta, it says nothing about model accuracy.

Counting follows the DPIA draft (docs/15-dpia-bozza.md): k distinct pseudonyms
per (cell, day type, slot) over the slot history (C1: one pseudonym per person,
cell and 28-day epoch, so a 4-week beta inside one epoch counts each tester once
per cell); C9 caps one event per person, cell and day.

Usage:
  .venv/bin/python scripts/beta_density.py --city milano
  .venv/bin/python scripts/beta_density.py --testers 20 --events 5 --cells 30 \
      --resolutions 9 8 --slot-minutes 30 180 --mission-share 0 0.5 --out /tmp/x.md
"""
import argparse
import itertools
import random
import statistics
import sys
from collections import defaultdict
from pathlib import Path

import h3

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from parking_core.config import load_city  # noqa: E402

DAY_TYPES = ("weekday",) * 5 + ("saturday", "holiday")  # day % 7 -> day type
# Relative demand for a parking search by hour (07-22). Assumption, not data.
HOUR_PROFILE = {7: 2, 8: 4, 9: 3, 10: 2, 11: 2, 12: 2, 13: 2, 14: 2, 15: 2,
                16: 2, 17: 3, 18: 4, 19: 4, 20: 3, 21: 2}
START_HOUR, END_HOUR = 7, 22
ANCHOR_TIMES = ((8.5, 0.75), (19.0, 1.0))  # (mean hour, sd): work arrival, home arrival


def beta_area(center: tuple[float, float], n_cells: int, resolution: int = 9) -> list[str]:
    """The n_cells res-9 cells closest to the center (grid rings, ties by id)."""
    origin = h3.latlng_to_cell(center[0], center[1], resolution)
    ring, cells = 0, []
    while len(cells) < n_cells:
        cells += sorted(h3.grid_ring(origin, ring))
        ring += 1
    return cells[:n_cells]


def slot_of(hour: float, width: int) -> int:
    return int((hour - START_HOUR) * 60 // width)


def slots_per_day(width: int) -> int:
    return -(-(END_HOUR - START_HOUR) * 60 // width)


def profile_hour(rng: random.Random) -> float:
    hour = rng.choices(list(HOUR_PROFILE), weights=list(HOUR_PROFILE.values()))[0]
    return hour + rng.random()


def clip(hour: float) -> float:
    return min(max(hour, START_HOUR), END_HOUR - 1e-6)


def simulate(a: argparse.Namespace, n: int, e: float, z: int, res: int, width: int,
             mission: float, seed: int) -> dict:
    rng = random.Random(seed)
    area = beta_area(a.center, z)
    to_res = {c: (c if res == 9 else h3.cell_to_parent(c, res)) for c in area}
    agg_cells = sorted(set(to_res.values()))
    children = defaultdict(list)
    for c in area:
        children[to_res[c]].append(c)
    days = a.weeks * 7
    weekdays = [d for d in range(days) if DAY_TYPES[d % 7] == "weekday"]
    per_tester = round(e * a.weeks)
    n_mission = round(per_tester * mission)
    # Missions: weekday cell-slots chosen by us, assigned round-robin so every
    # target receives distinct testers. Spread evenly over the whole area.
    targets = [(c, s) for s in range(slots_per_day(width)) for c in agg_cells]
    rng.shuffle(targets)
    events = []  # (tester, res9 cell, day, hour)
    for t in range(n):
        anchors = [rng.choice(area) for _ in ANCHOR_TIMES]
        for j in range(per_tester):
            if j < n_mission and targets:
                if rng.random() > a.compliance:
                    continue
                cell, s = targets[(t * n_mission + j) % len(targets)]
                hour = START_HOUR + (s + rng.random()) * width / 60
                events.append((t, rng.choice(children[cell]), rng.choice(weekdays), clip(hour)))
                continue
            if rng.random() > a.in_area:
                continue  # outside the beta area: never reaches k there
            day = rng.randrange(days)
            if rng.random() < a.habit:
                i = rng.randrange(len(anchors))
                mean, sd = ANCHOR_TIMES[i]
                events.append((t, anchors[i], day, clip(rng.gauss(mean, sd))))
            else:
                events.append((t, rng.choice(area), day, profile_hour(rng)))
    seen, history, per_day = set(), defaultdict(set), defaultdict(set)
    kept = []
    for t, cell, day, hour in events:
        if (t, cell, day) in seen:  # C9
            continue
        seen.add((t, cell, day))
        if rng.random() < a.holdout:
            continue  # validation quota: never enters the published model
        key = (to_res[cell], DAY_TYPES[day % 7], slot_of(hour, width))
        history[key].add(t)
        per_day[key + (day,)].add(t)
        kept.append(key)
    visible = {key for key, ids in history.items() if len(ids) >= a.k}
    wd_visible = sum(1 for key in visible if key[1] == "weekday")
    wd_total = len(agg_cells) * slots_per_day(width)
    return {
        "visible": len(visible),
        "wd_cov": wd_visible / wd_total,
        "event_share": sum(key in visible for key in kept) / len(kept) if kept else 0.0,
        "per_day": sum(1 for ids in per_day.values() if len(ids) >= a.k),
        "cells": len(agg_cells),
        "outcomes": len(kept),
    }


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--city", default="milano")
    p.add_argument("--center", type=lambda s: tuple(map(float, s.split(","))),
                   help="LAT,LNG of the beta area; default: centre of the city bbox")
    p.add_argument("--testers", type=int, nargs="+", default=[10, 20, 50, 100])
    p.add_argument("--events", type=float, nargs="+", default=[5],
                   help="outcomes per tester per week")
    p.add_argument("--cells", type=int, nargs="+", default=[30], help="beta area, res-9 cells")
    p.add_argument("--resolutions", type=int, nargs="+", default=[9, 8])
    p.add_argument("--slot-minutes", type=int, nargs="+", default=[30, 180])
    p.add_argument("--mission-share", type=float, nargs="+", default=[0.0, 0.5])
    p.add_argument("--weeks", type=int, default=4)
    p.add_argument("--k", type=int, help="default: privacy.min_contributors of the city")
    p.add_argument("--habit", type=float, default=0.6, help="share of free events at own anchors")
    p.add_argument("--in-area", type=float, default=0.8, help="share of free events inside the area")
    p.add_argument("--compliance", type=float, default=0.8, help="share of missions carried out")
    p.add_argument("--holdout", type=float, default=0.10, help="validation quota excluded from k")
    p.add_argument("--runs", type=int, default=20)
    p.add_argument("--seed", type=int, default=20261114)
    p.add_argument("--out", type=Path)
    a = p.parse_args(argv)
    city = load_city(a.city)
    a.k = a.k or city["privacy"]["min_contributors"]
    if a.center is None:
        b = city["grid"]["bbox"]
        a.center = ((b["south"] + b["north"]) / 2, (b["west"] + b["east"]) / 2)

    lines = [
        "SIMULAZIONE SINTETICA: dimensiona la beta, non misura accuratezza.",
        f"k={a.k} weeks={a.weeks} habit={a.habit} in_area={a.in_area} compliance={a.compliance} "
        f"holdout={a.holdout} runs={a.runs} seed={a.seed}",
        "",
        "| N | E/sett | Z (res9) | res | fascia | missioni | celle | esiti | celle-fascia ≥k "
        "| copertura feriale | quota esiti visibili | ≥k nel singolo giorno |",
        "|" + "---|" * 12,
    ]
    for n, e, z, res, width, m in itertools.product(a.testers, a.events, a.cells,
                                                     a.resolutions, a.slot_minutes, a.mission_share):
        runs = [simulate(a, n, e, z, res, width, m, a.seed + r) for r in range(a.runs)]
        avg = {key: statistics.mean(r[key] for r in runs) for key in runs[0]}
        lines.append(
            f"| {n} | {e:g} | {z} | {res} | {width} min | {m:.0%} | {avg['cells']:.0f} "
            f"| {avg['outcomes']:.0f} | {avg['visible']:.1f} | {avg['wd_cov']:.0%} "
            f"| {avg['event_share']:.0%} | {avg['per_day']:.1f} |")
    text = "\n".join(lines) + "\n"
    if a.out:
        a.out.write_text(text, encoding="utf-8")
    print(text, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
