"""Publication job: events -> outcomes -> grid.json + forecast.json.

Usage: python -m backend.publish_job <city> [--retention]
"""
import json
import os
import sys
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from parking_core.config import load_city
from parking_core.model import Outcome
from parking_core.privacy import Admission
from parking_core.publish import build_forecast, build_grid, write_forecast, write_grid

from .app import ROOT, run_retention
from .store import SqliteStore, current_step, oldest_live_step


def to_outcomes(events: list[dict], config: dict, now: datetime) -> list[Outcome]:
    """Success = bucket 0 or 1 (<= target).

    The history knows only the week, so its outcomes are at least a day old and
    never "live". Live outcomes come from the short-lived `live` rows (5-minute
    step), which exist only inside the live window (T-040: no times in the history).
    """
    interval = config["publish"]["interval_minutes"]
    window = config["model"]["live_window_minutes"]
    now_step = current_step(now, interval)
    result = []
    for e in events:
        step = e.get("live_step")
        if step is not None and 0 <= (now_step - step) * interval <= window:
            age = (now_step - step) * interval / 1440
        else:  # mid-week estimate of the age, never below one day
            age = max(1.0, (now.date() - date.fromisoformat(e["week"])).days - 3.0)
        result.append(Outcome(e["cell"], (e["day_type"], e["slot_index"]), e["search_bucket"] <= 1,
                              float(age), e["pid"]))
    return result


def publish(store, config: dict, out_dir: Path, now: datetime | None = None) -> tuple[Path, Path]:
    now = now or datetime.now(ZoneInfo(config["timezone"]))
    store.purge_live(oldest_live_step(now, config["publish"]["interval_minutes"],
                                      config["model"]["live_window_minutes"]))
    outcomes = to_outcomes(store.events(), config, now)
    admission = Admission.from_config(config, store.load_admitted())
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
