"""Backend tests. All event data here is SYNTHETIC: it tests code, not accuracy."""
import json
import sqlite3
from datetime import date, datetime
from zoneinfo import ZoneInfo

import pytest
from fastapi.testclient import TestClient

from backend.app import create_app, run_retention
from backend.publish_job import publish
from backend.store import SqliteStore
from parking_core import grid
from parking_core.config import load_city

CITY = "milano"  # test fixture only; backend code never names a city


@pytest.fixture(scope="module")
def config():
    return load_city(CITY)


@pytest.fixture(scope="module")
def cell(config):
    cells = grid.cells_for_bbox(config["grid"]["bbox"], config["grid"]["h3_resolution"])
    return cells[len(cells) // 2]


@pytest.fixture
def env(tmp_path, config):
    store = SqliteStore(str(tmp_path / "e.sqlite3"))
    app = create_app(CITY, out_dir=tmp_path / "out", store=store)
    return TestClient(app), store, tmp_path, tmp_path / "e.sqlite3"


def event(cell, pid="a" * 20, **kw):
    base = {"type": "parked", "cell": cell, "slot_day_type": "weekday", "slot_index": 20,
            "search_bucket": 0, "pid": pid, "app_version": "0.1.0"}
    base.update(kw)
    return base


def test_valid_event_accepted(env, cell):
    client, store, *_ = env
    assert client.post("/v1/events", json=event(cell)).status_code == 202
    assert len(store.events()) == 1


@pytest.mark.parametrize("extra", [{"lat": 45.46}, {"lng": 9.19}, {"ip": "1.2.3.4"},
                                    {"timestamp": "2026-01-01T10:00:00"}, {"coordinates": [1, 2]}])
def test_extra_fields_rejected(env, cell, extra):
    client, store, *_ = env
    assert client.post("/v1/events", json={**event(cell), **extra}).status_code == 422
    assert store.events() == []


@pytest.mark.parametrize("patch", [
    {"search_bucket": 4}, {"search_bucket": None}, {"pid": "XYZ"}, {"pid": "a" * 21},
    {"cell": "45.46,9.19"}, {"cell": "8928308280fffff"}, {"vehicle_class": "truck"},
    {"slot_day_type": "funday"}, {"slot_index": 999}, {"type": "left"},
])
def test_invalid_values_rejected(env, cell, patch):
    client, *_ = env
    assert client.post("/v1/events", json={**event(cell), **patch}).status_code == 422


def test_departures_are_not_collected(env, cell):
    client, store, *_ = env
    body = event(cell, type="left")
    body.pop("search_bucket")
    assert client.post("/v1/events", json=body).status_code == 422
    assert store.events() == []


def test_vehicle_class_is_counted_not_stored(env, cell):
    client, store, _, db = env
    assert client.post("/v1/events", json=event(cell, vehicle_class="moto")).status_code == 202
    assert store.vehicle_totals() == {("moto", 0): 1}
    with sqlite3.connect(db) as con:
        assert "vehicle_class" not in [r[1] for r in con.execute("PRAGMA table_info(events)")]


def test_rate_limit_per_pid_type_cell(env, cell):
    client, *_ = env
    assert client.post("/v1/events", json=event(cell)).status_code == 202
    assert client.post("/v1/events", json=event(cell)).status_code == 429


def test_no_time_or_ip_columns(env, cell):
    client, _, _, db = env
    client.post("/v1/events", json=event(cell))
    with sqlite3.connect(db) as con:
        for table in ("events", "admitted"):
            cols = [r[1].lower() for r in con.execute(f"PRAGMA table_info({table})")]
            assert not [c for c in cols if any(w in c for w in ("ip", "agent", "time", "lat", "lng", "hour"))
                        and c != "slot_index"], cols
            assert not {"day", "vehicle_class", "app_version", "type"} & set(cols)
        (week,) = con.execute("SELECT week FROM events").fetchone()
    assert date.fromisoformat(week).weekday() == 0  # a Monday: week granularity only


def test_retention(env, cell, config):
    _, store, *_ = env
    store.add_event({**event(cell), "slot_day_type": "weekday"}, date(2026, 1, 1))  # week of Dec 29
    store.add_event({**event(cell, pid="b" * 20), "slot_day_type": "weekday"}, date(2026, 2, 20))
    deleted = run_retention(store, config, today=date(2026, 2, 25))
    assert deleted == 1 and len(store.events()) == 1


def test_full_flow_event_to_grid(env, cell, config):
    client, store, tmp, _ = env
    k = config["privacy"]["min_contributors"]
    now = datetime(2026, 3, 4, 10, 30, tzinfo=ZoneInfo(config["timezone"]))  # a Wednesday, admission step
    slots_per_hour = 60 // config["time"]["slot_minutes"]
    index = now.hour * slots_per_hour + now.minute // config["time"]["slot_minutes"]
    for i in range(k + 1):
        body = event(cell, pid=f"{i:020x}", slot_index=index, search_bucket=0)
        assert client.post("/v1/events", json=body).status_code == 202
    # Events were stored "today" by the server clock; align them with the fixed publish time.
    with sqlite3.connect(tmp / "e.sqlite3") as con:
        con.execute("UPDATE events SET week = ?", (now.date().isoformat(),))
        con.execute("DELETE FROM live")  # fixed publish time: only the history is under test here
    grid_path, forecast_path = publish(store, config, tmp / "out", now)
    published = json.loads(grid_path.read_text())
    assert published["cells"][cell][3] is True  # based on user data
    assert published["cells"][cell][1] == "high"
    assert client.get(f"/v1/grid/{CITY}").json()["city"] == CITY
    forecast = client.get(f"/v1/forecast/{CITY}").json()
    assert cell in forecast["slots"]["weekday"][str(index)]
    # Admission state is persisted, never published.
    assert len(store.load_admitted()[cell]) == k + 1


def test_published_files_have_no_pid_or_counts(env, cell, config):
    client, store, tmp, _ = env
    now = datetime(2026, 3, 4, 10, 30, tzinfo=ZoneInfo(config["timezone"]))
    pids = [f"{i + 100:020x}" for i in range(7)]
    for pid in pids:
        client.post("/v1/events", json=event(cell, pid=pid, slot_index=20))
    with sqlite3.connect(tmp / "e.sqlite3") as con:
        con.execute("UPDATE events SET week = ?", (now.date().isoformat(),))
    paths = publish(store, config, tmp / "out", now)
    for path in paths:
        text = path.read_text()
        assert not any(pid in text for pid in pids)
        for key in ("pid", "contributor", "count", "n_outcomes", "n_contributors"):
            assert key not in text
    # cells hold [class value, level, reliability, user flag] only
    assert all(len(v) == 4 for v in json.loads(paths[0].read_text())["cells"].values())


def test_static_files_404_and_traversal(env):
    client, *_ = env
    assert client.get("/v1/grid/nowhere").status_code == 404
    assert client.get("/v1/grid/..%2F..%2Fetc").status_code == 404
