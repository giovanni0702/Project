"""Publication job: events -> outcomes -> grid.json + forecast.json.

Usage: python -m backend.publish_job <city> [--retention]
"""
import json
import os
import sys
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from parking_core import slots as slots_mod
from parking_core.config import load_city
from parking_core.model import Outcome
from parking_core.privacy import Admission
from parking_core.publish import build_forecast, build_grid, write_forecast, write_grid

from .app import ROOT, run_retention
from .store import SqliteStore


def to_outcomes(events: list[dict], config: dict, now: datetime) -> list[Outcome]:
    """Only 'parked' events carry a search result. Success = bucket 0 or 1 (<= target).

    The arrival time is unknown: an event counts as "live" only if it was sent
    today in the current or previous slot; otherwise its age is whole days
    (at least 1 for earlier slots of today, so it never counts as live).
    """
    slot_minutes = config["time"]["slot_minutes"]
    day_type, index = slots_mod.slot_key(now, slot_minutes)
    result = []
    for e in events:
        if e["type"] != "parked":
            continue
        age = (now.date() - date.fromisoformat(e["day"])).days
        if age == 0 and not (e["day_type"] == day_type and index - 1 <= e["slot_index"] <= index):
            age = 1
        result.append(Outcome(e["cell"], (e["day_type"], e["slot_index"]), e["search_bucket"] <= 1,
                              float(age), e["pid"]))
    return result


def publish(store, config: dict, out_dir: Path, now: datetime | None = None) -> tuple[Path, Path]:
    now = now or datetime.now(ZoneInfo(config["timezone"]))
    outcomes = to_outcomes(store.events(), config, now)
    admission = Admission(config["privacy"]["admission_batch"], store.load_admitted())
    previous = None
    old = out_dir / config["id"] / "grid.json"
    if old.is_file():
        previous = {c: v[1] for c, v in json.loads(old.read_text())["cells"].items()}
    grid_payload = build_grid(config, outcomes, now, previous, admission)
    forecast_payload = build_forecast(config, outcomes, now, admission)
    store.save_admitted(admission.admitted, now.date())
    return write_grid(grid_payload, out_dir), write_forecast(forecast_payload, out_dir)


def main(argv: list[str]) -> None:
    config = load_city(argv[1])
    store = SqliteStore(os.environ.get("PARKING_DB", str(ROOT / "data/backend/events.sqlite3")))
    out_dir = Path(os.environ.get("PARKING_OUT", ROOT / "build/grid"))
    if "--retention" in argv:
        run_retention(store, config)
    publish(store, config, out_dir)


if __name__ == "__main__":
    main(sys.argv)
