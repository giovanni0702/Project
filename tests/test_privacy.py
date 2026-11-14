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


def simulate(cycles=72, agents=20, seed=11):
    """20 agents report in 3 busy cells; a grid is published every 5 minutes."""
    rng = random.Random(seed)
    busy = [CELLS[400], CELLS[401], CELLS[900]]
    secrets = [f"agent-{i}".encode() for i in range(agents)]
    owner, events, grids, admission, levels = {}, [], [], Admission(CITY["privacy"]["admission_batch"]), {}
    for cycle in range(cycles):
        now = START + timedelta(minutes=5 * cycle)
        for agent in range(agents):
            if rng.random() < 0.08:
                cell = rng.choice(busy)
                pid = pseudonym(secrets[agent], "parked", cell, 0)
                owner[pid] = agent
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
    admission, outcomes, levels, flip = Admission(CITY["privacy"]["admission_batch"]), [], {}, None
    for cycle in range(6):
        now = NOW0 + timedelta(minutes=5 * cycle)
        outcomes += [Outcome(TARGET, SLOT, rng.random() < 0.5, 0.0, who) for who in arrivals.get(cycle, [])]
        aged = [replace(o, age_days=0.0) for o in outcomes]
        payload = build_grid(CITY, aged, now=now, previous_levels=levels, admission=admission)
        levels = {c: v[1] for c, v in payload["cells"].items()}
        if flip is None and payload["cells"][TARGET][3]:
            flip = cycle
    return flip, t_a, t_b


@pytest.mark.xfail(strict=True, reason="T-039 attack 1: in a block of 2 the cell turns user-based exactly "
                   "when the second member arrives, so the first member learns the other's arrival cycle")
def test_attack_1_block_member_learns_when_the_other_contributed():
    trials = [run_block_scenario(seed) for seed in range(40)]
    assert all(flip is not None for flip, _, _ in trials), "scenario never reached k"
    exact = sum(flip == t_b for flip, _, t_b in trials) / len(trials)
    assert exact < 0.2, f"attacker pins the other member's arrival cycle in {exact:.0%} of trials"


@pytest.mark.xfail(strict=True, reason="T-039 attack 2: the grid timeline gives the arrival time of the "
                   "last member of every admitted block (to the 5-minute publication step)")
def test_attack_2_saved_grids_reveal_when_a_block_arrived():
    flips = aligned = 0
    for (old, _, _), (new, newly, _) in zip(GRIDS, GRIDS[1:]):
        for cell, value in new["cells"].items():
            if value[3] and not old["cells"][cell][3]:           # cell becomes "based on user data"
                flips += 1
                aligned += bool(newly.get(cell))                  # same cycle as a block admission
    assert flips > 0, "simulation never produced a flip: the test would prove nothing"
    assert aligned / flips < 0.5, f"{aligned}/{flips} flips fall exactly on a block's arrival cycle"


def test_attack_3_contributions_below_k_do_not_leak_to_neighbours():
    """Four admitted people (below k) with all-success outcomes must not move any published cell."""
    cell = CELLS[600]
    people = [Outcome(cell, SLOT, True, 0.0, f"p{i}") for i in range(CITY["privacy"]["min_contributors"] - 1)]
    now = NOW0
    quiet = build_grid(CITY, [], now=now, admission=Admission(CITY["privacy"]["admission_batch"]))
    loud = build_grid(CITY, people, now=now, admission=Admission(CITY["privacy"]["admission_batch"]))
    assert loud["cells"] == quiet["cells"]
    assert not loud["cells"][cell][3]


@pytest.mark.xfail(strict=True, reason="T-039 attack 6: k counts pseudonyms, but the pseudonym changes every "
                   "28-day epoch, so 3 real people straddling an epoch boundary pass k=5")
def test_attack_6_k_counts_people_not_pseudonyms_across_epochs():
    secrets = [f"epoch-agent-{i}".encode() for i in range(3)]
    outcomes = [Outcome(TARGET, SLOT, True, 0.0, pseudonym(s, "parked", TARGET, day))
                for s in secrets for day in (27, 28)]            # same person, two epochs, two pids
    assert len({o.contributor for o in outcomes}) >= K           # what the server sees
    payload = build_grid(CITY, outcomes, now=NOW0, admission=Admission(CITY["privacy"]["admission_batch"]))
    assert not payload["cells"][TARGET][3], "3 real people published as user data with k=5"


def fill_store(seed, with_vehicle, day_bucket=None):
    """20 synthetic commuters, 20 weekdays, through the real SqliteStore schema.
    Returns (store, owner: pid -> agent, home, work)."""
    rng = random.Random(seed)
    store, owner = SqliteStore(":memory:"), {}
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
                store.add_event({"type": typ, "cell": cell, "slot_day_type": "weekday", "slot_index": slot,
                                 "search_bucket": 1 if typ == "parked" else None, "vehicle_class": vehicle,
                                 "pid": pid, "app_version": "0.1"}, seen)
    return store, owner


@pytest.mark.xfail(strict=True, reason="T-039 attack 4: vehicle_class stored with every event makes the only "
                   "motorcycle among 20 testers a stable key that joins its events across cells")
def test_attack_4_rare_vehicle_class_links_events_across_cells():
    store, owner = fill_store(seed=3, with_vehicle=True)
    events = store.events()
    population = {}
    for e in events:
        population.setdefault(e["vehicle_class"], set()).add(owner[e["pid"]])
    rare = [c for c, agents in population.items() if len(agents) < K]
    victim_events = [e for e in events if e["vehicle_class"] in rare and len(population[e["vehicle_class"]]) == 1]
    cells_joined = {e["cell"] for e in victim_events}
    assert len(cells_joined) <= 1, f"{len(victim_events)} events in {len(cells_joined)} cells joined by one rare class"


def link_left_to_parked(store, owner):
    """Join a 'left' pseudonym to a 'parked' pseudonym of another cell when the next slot
    and the exact set of days match. Returns (links tried, links correct, agents covered)."""
    groups = {}
    for e in store.events():
        groups.setdefault((e["type"], e["cell"], e["pid"]), (e["slot_index"], set()))[1].add(e["day"])
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


@pytest.mark.xfail(strict=True, reason="T-039 attack 5: day + slot_index kept per event let the server join "
                   "'left' in one cell to 'parked' in another (same days, next slot) despite per-cell pid")
def test_attack_5_day_and_slot_link_departure_to_next_parking():
    store, owner = fill_store(seed=4, with_vehicle=False)
    tried, correct, covered = link_left_to_parked(store, owner)
    assert correct == 0, f"{correct} correct cross-cell links, {covered} of 20 agents joined"


def test_attack_5_control_week_granularity_breaks_the_link():
    """Control for the proposed fix: with the day coarsened to a week the same attack fails."""
    store, owner = fill_store(seed=4, with_vehicle=False, day_bucket=7)
    tried, correct, covered = link_left_to_parked(store, owner)
    assert correct <= 2, f"{correct} correct links even with week-only dates"
