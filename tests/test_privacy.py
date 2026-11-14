"""Re-identification checks on the core (DPIA draft section 9, attacks A and B,
plus the published-file scan). SYNTHETIC agents: a technical test, not accuracy.

Attacks C-E (linking, home/work, external knowledge) need the device and server
code and are added with them (T-034)."""
import json
import random
import re
from datetime import datetime, timedelta

from parking_core import grid, streets
from parking_core.config import load_city
from parking_core.model import Outcome
from parking_core.privacy import Admission, pseudonym
from parking_core.publish import build_grid

CITY = load_city("milano")
K = CITY["privacy"]["min_contributors"]
RES = CITY["grid"]["h3_resolution"]
CELLS = grid.cells_for_bbox(CITY["grid"]["bbox"], RES)
START = datetime(2026, 11, 16, 8, 0)


def test_pseudonym_unlinkable_across_cells_types_and_epochs():
    secret = b"device-secret"
    base = pseudonym(secret, "parked", CELLS[0], 100)
    assert base == pseudonym(secret, "parked", CELLS[0], 101)          # same epoch
    assert base != pseudonym(secret, "parked", CELLS[1], 100)          # other cell
    assert base != pseudonym(secret, "left", CELLS[0], 100)            # other type
    assert base != pseudonym(secret, "parked", CELLS[0], 100 + 28)     # next epoch
    assert base != pseudonym(b"other-device", "parked", CELLS[0], 100)


ARRIVALS: dict[tuple[str, int], int] = {}   # (cell, agent) -> cycle of the agent's first event there


def simulate(cycles=72, agents=20, seed=11):
    """20 agents report in 3 busy cells; a grid is published every 5 minutes."""
    rng = random.Random(seed)
    busy = [CELLS[400], CELLS[401], CELLS[900]]
    secrets = [f"agent-{i}".encode() for i in range(agents)]
    owner, events, grids, admission, levels = {}, [], [], Admission.from_config(CITY), {}
    for cycle in range(cycles):
        now = START + timedelta(minutes=5 * cycle)
        for agent in range(agents):
            if rng.random() < 0.08:
                cell = rng.choice(busy)
                pid = pseudonym(secrets[agent], "parked", cell, 0)
                owner[pid] = agent
                ARRIVALS.setdefault((cell, agent), cycle)
                events.append((now, cell, pid, rng.random() < 0.6))
        slot = ("weekday", (now.hour * 60 + now.minute) // CITY["time"]["slot_minutes"])
        outcomes = [Outcome(c, slot, ok, (now - t).total_seconds() / 86400, pid) for t, c, pid, ok in events]
        before = {c: set(ids) for c, ids in admission.admitted.items()}
        payload = build_grid(CITY, outcomes, now=now, previous_levels=levels, admission=admission)
        levels = {c: v[1] for c, v in payload["cells"].items()}
        newly = {c: {owner[p] for p in ids - before.get(c, set())} for c, ids in admission.admitted.items()}
        truth = {}
        for _, c, pid, _ in events:
            if pid in admission.admitted.get(c, ()):
                truth.setdefault(c, set()).add(owner[pid])
        grids.append((payload, newly, truth))
    return grids


GRIDS = simulate()


def test_attack_a_published_user_data_always_has_k_real_people():
    published = 0
    for payload, _, truth in GRIDS:
        for cell, value in payload["cells"].items():
            if value[3]:
                published += 1
                assert len(truth.get(cell, ())) >= K
    assert published > 0, "simulation never reached k: the test would prove nothing"


def test_attack_b_no_change_between_grids_comes_from_one_person():
    changed = 0
    for (old, _, _), (new, newly, _) in zip(GRIDS, GRIDS[1:]):
        for cell in new["cells"]:
            if new["cells"][cell] == old["cells"][cell]:
                continue
            around = [cell, *grid.neighbors(cell)]
            sizes = [len(newly.get(c, ())) for c in around if newly.get(c)]
            changed += 1
            assert all(size >= 2 for size in sizes), "a single new contributor moved the grid"
    assert changed > 0


def test_published_file_has_no_counts_ids_or_coordinates():
    payload = GRIDS[-1][0]
    text = json.dumps(payload)
    assert not re.search(r"\b(45|9)\.\d{3,}", text)            # no lat/lon
    assert "agent" not in text and "contributor" not in text
    assert set(payload) == {"city", "generated_at", "valid_minutes", "slot", "model_version",
                            "h3_resolution", "vehicle_odds", "cells"}
    allowed = set(CITY["display"]["class_values"].values())
    assert all(v[0] in allowed and len(v) == 4 for v in payload["cells"].values())


def test_street_pieces_are_split_by_cell():
    way = {"type": "way", "id": 1, "tags": {"name": "Via Test", "highway": "residential", "parking:both": "lane"},
           "geometry": [{"lat": 45.4640 + i * 0.0012, "lon": 9.1900} for i in range(8)]}
    pieces = streets.pieces_from_ways([way], RES)
    assert len(pieces) >= 2 and len({p["cell"] for p in pieces}) == len(pieces)
    assert all(len(p["line"]) >= 2 and p["parking"] == {"parking:both": "lane"} for p in pieces)
    assert pieces[0]["line"][-1] == pieces[1]["line"][0]        # pieces stay connected


# ---------------------------------------------------------------------------
# T-039: new attacks by the red team (fixed seeds, synthetic data only).
# A test marked xfail(strict=True) is an attack that SUCCEEDS today: the suite
# stays green, the flaw is tracked, and the test turns red as soon as it is fixed
# (then drop the marker). Report: reports/reid/2026-11-14.md
# ---------------------------------------------------------------------------
import pytest  # noqa: E402
from dataclasses import replace  # noqa: E402
from datetime import date  # noqa: E402

from backend.store import SqliteStore  # noqa: E402

SLOT = ("weekday", 16)
NOW0 = datetime(2026, 11, 16, 8, 0)
TARGET = CELLS[400]


def run_block_scenario(seed, base=4):
    """`base` people already admitted in TARGET (cycle 0), then A (tester, the attacker)
    contributes at cycle t_a and B at cycle t_b > t_a. One grid every 5 minutes.
    Returns (first cycle in which TARGET shows user data, t_a, t_b)."""
    rng = random.Random(seed)
    t_a = rng.randint(1, 4)
    t_b = rng.randint(t_a + 1, 5)
    arrivals = {0: [f"base{i}" for i in range(base)], t_a: ["A"], t_b: ["B"]}
    admission, outcomes, levels, flip = Admission.from_config(CITY), [], {}, None
    window = CITY["privacy"]["admission_interval_minutes"] // CITY["publish"]["interval_minutes"]
    for cycle in range(window + 1):   # up to and including the first admission step after the arrivals
        now = NOW0 + timedelta(minutes=5 * cycle)
        outcomes += [Outcome(TARGET, SLOT, rng.random() < 0.5, 0.0, who) for who in arrivals.get(cycle, [])]
        aged = [replace(o, age_days=0.0) for o in outcomes]
        payload = build_grid(CITY, aged, now=now, previous_levels=levels, admission=admission)
        levels = {c: v[1] for c, v in payload["cells"].items()}
        if flip is None and payload["cells"][TARGET][3]:
            flip = cycle
    return flip, t_a, t_b


def test_attack_1_block_member_learns_when_the_other_contributed():
    trials = [run_block_scenario(seed) for seed in range(40)]
    assert all(flip is not None for flip, _, _ in trials), "scenario never reached k"
    exact = sum(flip == t_b for flip, _, t_b in trials) / len(trials)
    assert exact < 0.2, f"attacker pins the other member's arrival cycle in {exact:.0%} of trials"


def test_attack_2_saved_grids_do_not_reveal_when_a_block_arrived():
    """A flip to "user data" is pinned to a member's arrival when it falls in the same
    publication step as the last arrival of the block that caused it (the original attack,
    measured on arrival time rather than on the admission cycle, which is now a fixed clock)."""
    flips = pinned = 0
    for step, ((old, _, _), (new, newly, _)) in enumerate(zip(GRIDS, GRIDS[1:]), start=1):
        for cell, value in new["cells"].items():
            if value[3] and not old["cells"][cell][3]:           # cell becomes "based on user data"
                flips += 1
                last = max(ARRIVALS[(cell, agent)] for agent in newly[cell])
                pinned += last == step                            # flip in the same step as the last arrival
    assert flips > 0, "simulation never produced a flip: the test would prove nothing"
    assert pinned / flips < 0.5, f"{pinned}/{flips} flips fall exactly on a block's arrival step"


def test_attack_3_contributions_below_k_do_not_leak_to_neighbours():
    """Four admitted people (below k) with all-success outcomes must not move any published cell."""
    cell = CELLS[600]
    people = [Outcome(cell, SLOT, True, 0.0, f"p{i}") for i in range(CITY["privacy"]["min_contributors"] - 1)]
    now = NOW0
    quiet = build_grid(CITY, [], now=now, admission=Admission.from_config(CITY))
    loud = build_grid(CITY, people, now=now, admission=Admission.from_config(CITY))
    assert loud["cells"] == quiet["cells"]
    assert not loud["cells"][cell][3]


def test_attack_6_k_counts_people_not_pseudonyms_across_epochs():
    secrets = [f"epoch-agent-{i}".encode() for i in range(3)]
    outcomes = [Outcome(TARGET, SLOT, True, 0.0, pseudonym(s, "parked", TARGET, day))
                for s in secrets for day in (27, 28)]            # same person, two epochs, two pids
    assert len({o.contributor for o in outcomes}) >= K           # what the server sees
    payload = build_grid(CITY, outcomes, now=NOW0, admission=Admission.from_config(CITY))
    assert not payload["cells"][TARGET][3], "3 real people published as user data with k=5"


def fill_store(seed, with_vehicle, day_bucket=None):
    """20 synthetic commuters, 20 weekdays, through the real SqliteStore schema.
    Returns (store, owner: pid -> agent, raw): `raw` is what the phones sent, before the store
    discards what it does not keep (rows: type, cell, pid, slot, day as sent)."""
    rng = random.Random(seed)
    store, owner, raw = SqliteStore(":memory:"), {}, []
    homes, works = CELLS[100:120], CELLS[200:205]
    classes = ["moto"] + ["small"] * 4 + ["medium"] * 12 + ["large"] * 3
    secrets = [f"commuter-{i}".encode() for i in range(20)]
    for agent in range(20):
        home, work = homes[agent], works[agent % 5]
        vehicle = classes[agent] if with_vehicle else None
        for d in range(20):
            if rng.random() > 0.75:
                continue
            day = date(2026, 11, 2) + timedelta(days=d)
            seen = day if day_bucket is None else day - timedelta(days=day.weekday() % day_bucket)
            for typ, cell, slot in (("left", home, 16), ("parked", work, 17), ("left", work, 35), ("parked", home, 36)):
                pid = pseudonym(secrets[agent], typ, cell, d)
                owner[pid] = agent
                raw.append((typ, cell, pid, slot, seen))
                store.add_event({"type": typ, "cell": cell, "slot_day_type": "weekday", "slot_index": slot,
                                 "search_bucket": 1 if typ == "parked" else None, "vehicle_class": vehicle,
                                 "pid": pid, "app_version": "0.1"}, seen)
    return store, owner, raw


def test_attack_4_rare_vehicle_class_links_events_across_cells():
    store, owner, _ = fill_store(seed=3, with_vehicle=True)
    events = store.events()
    population = {}
    for e in events:
        population.setdefault(e.get("vehicle_class"), set()).add(owner[e["pid"]])
    rare = [c for c, agents in population.items() if len(agents) < K]
    victim_events = [e for e in events if e.get("vehicle_class") in rare and len(population[e.get("vehicle_class")]) == 1]
    cells_joined = {e["cell"] for e in victim_events}
    assert len(cells_joined) <= 1, f"{len(victim_events)} events in {len(cells_joined)} cells joined by one rare class"


def link_left_to_parked(rows, owner):
    """Join a 'left' pseudonym to a 'parked' pseudonym of another cell when the next slot
    and the exact set of days match. `rows`: (type, cell, pid, slot, day).
    Returns (links tried, links correct, agents covered)."""
    groups = {}
    for typ, cell, pid, slot, day in rows:
        groups.setdefault((typ, cell, pid), (slot, set()))[1].add(day)
    lefts = [(k, v) for k, v in groups.items() if k[0] == "left"]
    parked = [(k, v) for k, v in groups.items() if k[0] == "parked"]
    tried = correct = 0
    covered = set()
    for (_, cell_l, pid_l), (slot_l, days_l) in lefts:
        match = [pid_p for (_, cell_p, pid_p), (slot_p, days_p) in parked
                 if cell_p != cell_l and slot_p == slot_l + 1 and days_p == days_l]
        if len(match) == 1:
            tried += 1
            hit = owner[match[0]] == owner[pid_l]
            correct += hit
            if hit:
                covered.add(owner[pid_l])
    return tried, correct, len(covered)


def stored_rows(store):
    """What the server can still use: the store's own rows (no type, no day: week only)."""
    return [("parked", e["cell"], e["pid"], e["slot_index"], e["week"]) for e in store.events()]


def test_attack_5_day_and_slot_link_departure_to_next_parking():
    store, owner, raw = fill_store(seed=4, with_vehicle=False)
    assert any(r[0] == "left" for r in raw)                   # the phones did send departures
    tried, correct, covered = link_left_to_parked(stored_rows(store), owner)
    assert correct == 0, f"{correct} correct cross-cell links, {covered} of 20 agents joined"
    assert all(len(e["week"]) == 10 and e["week"] >= "2026-11-02" for e in store.events())


def test_attack_5_control_week_granularity_alone_breaks_the_link():
    """Control, independent of dropping departures: even if 'left' were stored, week-only
    dates make the same attack fail (it succeeds with exact days: second assert)."""
    _, owner, raw = fill_store(seed=4, with_vehicle=False)
    weekly = [(t, c, p, sl, d - timedelta(days=d.weekday())) for t, c, p, sl, d in raw]
    _, correct, _ = link_left_to_parked(weekly, owner)
    assert correct <= 2, f"{correct} correct links even with week-only dates"
    _, exact, _ = link_left_to_parked(raw, owner)
    assert exact >= 10, "with exact days the attack must work, or the control proves nothing"
