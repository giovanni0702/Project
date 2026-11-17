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
    """The saved grids show when a block was admitted; the attacker guesses the arrival step
    of its last member (and of every member) to be that step. Immediate admission: 22/22 blocks
    and 30/49 members guessed right; with a fixed admission clock the guess is only chance level
    (about 1 step in the interval)."""
    flips = sum(1 for (old, _, _), (new, _, _) in zip(GRIDS, GRIDS[1:])
                for c, v in new["cells"].items() if v[3] and not old["cells"][c][3])
    assert flips > 0, "simulation never produced a flip: the test would prove nothing"
    blocks = last_hits = members = member_hits = 0
    for step, (_, newly, _) in enumerate(GRIDS):
        for cell, agents in newly.items():
            if agents:
                blocks += 1
                last_hits += max(ARRIVALS[(cell, a)] for a in agents) == step
                members += len(agents)
                member_hits += sum(ARRIVALS[(cell, a)] == step for a in agents)
    assert blocks >= 10 and members >= 30
    assert last_hits / blocks < 0.5, f"{last_hits}/{blocks} blocks: last arrival pinned to the admission step"
    assert member_hits / members < 0.25, f"{member_hits}/{members} members pinned to the admission step"


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


# ---------------------------------------------------------------------------
# T-040: mechanisms behind the corrections (each one proved by a test).
# ---------------------------------------------------------------------------
from backend.store import current_step, oldest_live_step  # noqa: E402
from parking_core.privacy import people_lower_bound  # noqa: E402

PRIVACY = CITY["privacy"]


def table_columns(store, table):
    return {r[1] for r in store.query(f"PRAGMA table_info({table})")}


def test_history_keeps_no_vehicle_version_type_or_exact_day():
    store, _, _ = fill_store(seed=3, with_vehicle=True)
    assert not {"vehicle_class", "app_version", "type", "day"} & table_columns(store, "events")
    assert all(e["week"] >= "2026-11-02" and len(e["week"]) == 10 for e in store.events())
    assert not any(e["slot_index"] in (16, 35) for e in store.events())   # 'left' slots: nothing stored


def test_attack_4_aggregate_vehicle_counts_cannot_be_linked_to_events():
    store, owner, raw = fill_store(seed=3, with_vehicle=True)
    cols = table_columns(store, "vehicle_outcomes")
    assert cols == {"week", "vehicle_class", "search_bucket", "n"}      # no cell, pid, event id, slot
    assert cols & table_columns(store, "events") == {"week", "search_bucket"}   # only coarse shared keys
    rows = store.query("SELECT week, vehicle_class, search_bucket, n FROM vehicle_outcomes")
    events = store.events()
    assert sum(n for *_, n in rows) == len(events)                        # still learns from every parked event
    # The only moto: the best the server can do is match a counter row to events of the same
    # week and bucket. Each row must fit at least k stored events (anonymity set), in >= 2 cells.
    for week, _, bucket, _ in rows:
        candidates = [e for e in events if e["week"] == week and e["search_bucket"] == bucket]
        assert len(candidates) >= K and len({e["cell"] for e in candidates}) >= 2
    assert {c for (c, _) in store.vehicle_totals()} == {"moto", "small", "medium", "large"}


def test_daily_rate_limit_table_and_live_rows_do_not_outlive_their_window():
    store = SqliteStore(":memory:")
    base = {"type": "parked", "cell": CELLS[10], "slot_day_type": "weekday", "slot_index": 20,
            "search_bucket": 0, "pid": "0000" + "a" * 16, "app_version": "0.1"}
    assert store.add_event(base, date(2026, 11, 16), live_step=1000)
    assert not store.add_event(base, date(2026, 11, 16), live_step=1001)        # C9 still enforced
    assert store.add_event({**base, "pid": "0000" + "b" * 16}, date(2026, 11, 17), live_step=1005)
    assert store.query("SELECT COUNT(*) FROM daily_seen WHERE day < '2026-11-17'") == [(0,)]
    step_min, window = CITY["publish"]["interval_minutes"], CITY["model"]["live_window_minutes"]
    assert store.purge_live(1000 + -(-window // step_min) + 1) == 2
    assert all(e["live_step"] is None for e in store.events())            # history: no time at all
    now = datetime(2026, 11, 16, 12, 0).astimezone()
    assert oldest_live_step(now, step_min, window) == current_step(now, step_min) - -(-window // step_min)


def test_retention_never_keeps_more_than_the_declared_days():
    store = SqliteStore(":memory:")
    base = {"type": "parked", "cell": CELLS[10], "slot_day_type": "weekday", "slot_index": 20, "search_bucket": 0}
    today = date(2026, 12, 1)
    days = PRIVACY["raw_retention_days"]
    for back in range(0, days + 10):
        store.add_event({**base, "pid": f"{back:020x}"}, today - timedelta(days=back))
    store.delete_older_than(today - timedelta(days=days))
    kept = {e["week"] for e in store.events()}
    assert kept and min(kept) >= (today - timedelta(days=days + 6)).isoformat()   # weeks, never older than ~30 d
    assert min(kept) >= (today - timedelta(days=days)).isoformat()


def test_attack_6_five_pseudonyms_of_one_epoch_are_published_but_not_straddling_ones():
    same = [Outcome(TARGET, SLOT, True, 0.0, pseudonym(f"s{i}".encode(), "parked", TARGET, 30)) for i in range(K)]
    published = build_grid(CITY, same, now=NOW0, admission=Admission.from_config(CITY))
    assert published["cells"][TARGET][3], "cost check: k pseudonyms of one epoch must still publish"
    split = same[:K - 1] + [Outcome(TARGET, SLOT, True, 0.0, pseudonym(b"s0", "parked", TARGET, 60))]
    blocked = build_grid(CITY, split, now=NOW0, admission=Admission.from_config(CITY))
    assert not blocked["cells"][TARGET][3]
    assert people_lower_bound([o.contributor for o in split]) == K - 1


def test_attack_6_one_person_in_two_epochs_does_not_make_a_block():
    two = [Outcome(TARGET, SLOT, True, 0.0, pseudonym(b"solo", "parked", TARGET, d)) for d in (27, 28)]
    admission = Admission.from_config(CITY)
    admission.filter(two, now=NOW0)
    assert admission.admitted == {}


def test_admission_happens_only_at_the_fixed_clock_steps():
    step, interval = CITY["publish"]["interval_minutes"], PRIVACY["admission_interval_minutes"]
    batch = [Outcome(TARGET, SLOT, True, 0.0, f"p{i}") for i in range(PRIVACY["admission_batch"])]
    opened = []
    for cycle in range(2 * interval // step + 1):
        admission = Admission.from_config(CITY)
        admission.filter(batch, now=NOW0 + timedelta(minutes=step * cycle))
        opened.append(bool(admission.admitted))
    assert [i for i, o in enumerate(opened) if o] == [i for i in range(len(opened)) if i % (interval // step) == 0]
    assert not Admission.from_config(CITY).filter(batch, now=None)       # no clock: nothing enters


def test_admission_interval_leaves_live_time_for_new_contributors():
    """Interval + maximum phone send delay must stay below the live window, or a newly
    admitted outcome would already be stale; the interval must be a whole number of steps."""
    interval, delay = PRIVACY["admission_interval_minutes"], PRIVACY["send_delay_max_minutes"]
    assert interval + delay < CITY["model"]["live_window_minutes"]
    assert interval % CITY["publish"]["interval_minutes"] == 0
    assert 1440 % interval == 0


# ---------------------------------------------------------------------------
# T-047: independent re-test of the T-040 fixes, attacks D and E of the DPIA (section 9)
# and the residual "already admitted contributors enter the live estimate at once".
# xfail(strict=True) = attack that SUCCEEDS today. Report: reports/reid/2026-11-17.md
# ---------------------------------------------------------------------------
def commuters(seed, n_agents, activity, days=20):
    """Synthetic commuters through the real SqliteStore: work parked at slot 17, home parked at slot 36.
    Returns (store, owner: pid -> agent, home: agent -> cell)."""
    rng = random.Random(seed)
    store, owner, home = SqliteStore(":memory:"), {}, {}
    secrets = [f"t047-{seed}-{i}".encode() for i in range(n_agents)]
    for agent in range(n_agents):
        home[agent], work = CELLS[300 + agent], CELLS[500 + agent % 4]
        for d in range(days):
            if rng.random() > activity:
                continue
            day = date(2026, 11, 2) + timedelta(days=d)
            for cell, slot in ((work, 17), (home[agent], 36)):
                pid = pseudonym(secrets[agent], "parked", cell, d)
                owner[pid] = agent
                store.add_event({"type": "parked", "cell": cell, "slot_day_type": "weekday", "slot_index": slot,
                                 "search_bucket": 1, "pid": pid, "app_version": "0.1"}, day)
    return store, owner, home


def pid_profiles(store):
    """What the server holds per pseudonym: (cell, slots, set of weeks)."""
    prof = {}
    for e in store.events():
        cell, slots_, weeks = prof.setdefault(e["pid"], (e["cell"], set(), set()))
        slots_.add(e["slot_index"])
        weeks.add(e["week"])
    return prof


SPARSE = [(1, 0.75), pytest.param(2, 0.25, marks=pytest.mark.xfail(strict=True, reason="T-047 attack D: with few active days the set of weeks is a quasi-identifier and joins work and home pseudonyms")),
          pytest.param(3, 0.1, marks=pytest.mark.xfail(strict=True, reason="T-047 attack D/E: same, sparse activity"))]


@pytest.mark.parametrize("seed,activity", SPARSE)
def test_attack_d_home_cell_guess_is_not_better_than_chance(seed, activity):
    """Attacker links each evening pseudonym (slot 36 = home) to the unique morning pseudonym (slot 17 = work)
    of another cell with the same set of weeks, and so names a home for a person. Precision must not exceed
    chance (1 / number of homes) + 5 points."""
    store, owner, home = commuters(seed, n_agents=20, activity=activity)
    prof = pid_profiles(store)
    work = {p: v for p, v in prof.items() if 17 in v[1]}
    tried = correct = 0
    for pid_w, (cell_w, _, weeks_w) in work.items():
        cand = [p for p, (c, s, w) in prof.items() if 36 in s and c != cell_w and w == weeks_w]
        if len(cand) == 1:
            tried += 1
            correct += owner[cand[0]] == owner[pid_w]
    chance = 1 / 20
    assert tried == 0 or correct / tried <= chance + 0.05, f"home guessed right {correct}/{tried} (chance {chance:.0%})"


@pytest.mark.parametrize("seed,activity", SPARSE)
def test_attack_e_known_event_does_not_reveal_other_events_of_the_same_person(seed, activity):
    """Attacker knows one event of a person (cell, slot, weeks, from a friend or a photo). Looking at every other
    pseudonym of another cell whose weeks match, he must never end up with a single candidate that is the person."""
    store, owner, _ = commuters(seed, n_agents=20, activity=activity)
    prof = pid_profiles(store)
    found = set()
    for pid, (cell, _, weeks) in prof.items():
        cand = [p for p, (c, _, w) in prof.items() if c != cell and w == weeks]
        if len(cand) == 1 and owner[cand[0]] == owner[pid]:
            found.add(owner[pid])
    assert not found, f"{len(found)} of 20 persons: another event identified from one known event"


def test_attack_e_pseudonym_never_spans_two_cells():
    store, _, _ = commuters(1, 20, 0.75)
    cells_per_pid = {}
    for e in store.events():
        cells_per_pid.setdefault(e["pid"], set()).add(e["cell"])
    assert all(len(c) == 1 for c in cells_per_pid.values())


def residual_diff(n_admitted, seed):
    """Cell with `n_admitted` people admitted at an admission step. At the next 5-minute step (not an admission
    step) one of them contributes a new report (a failure, against old successes). Returns (grid cell without
    the report, grid cell with it)."""
    rng = random.Random(seed)
    people = [f"adm{i}" for i in range(n_admitted)]
    old = [Outcome(TARGET, SLOT, rng.random() < 0.9, 0.5, p) for p in people]
    result = []
    for extra in (False, True):
        admission, levels = Admission.from_config(CITY), {}
        build_grid(CITY, old, now=NOW0, previous_levels=levels, admission=admission)     # admission step
        later = NOW0 + timedelta(minutes=CITY["publish"]["interval_minutes"])
        fresh = [Outcome(TARGET, SLOT, False, 0.0, people[0])] if extra else []
        payload = build_grid(CITY, old + fresh, now=later, previous_levels=levels, admission=admission)
        result.append(payload["cells"][TARGET])
    return result


@pytest.mark.xfail(strict=True, reason="T-047 residual 1: an already admitted contributor enters the live estimate "
                   "at every 5-minute step, so one person can change a published cell (differencing)")
def test_attack_residual_admitted_contributor_moves_live_grid_at_once():
    changed = sum(a != b for a, b in (residual_diff(n, s) for n in (5, 6, 8) for s in range(20)))
    assert changed == 0, f"{changed}/60 variants: one admitted person's report changed the published cell"


def test_attack_residual_control_new_people_do_not_enter_outside_the_window():
    """Control: unadmitted people reporting between admission steps change nothing (T-040 fix holds)."""
    later = NOW0 + timedelta(minutes=CITY["publish"]["interval_minutes"])
    people = [Outcome(TARGET, SLOT, False, 0.0, f"new{i}") for i in range(8)]
    quiet = build_grid(CITY, [], now=later, admission=Admission.from_config(CITY))
    loud = build_grid(CITY, people, now=later, admission=Admission.from_config(CITY))
    assert loud["cells"] == quiet["cells"]
