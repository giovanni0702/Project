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
