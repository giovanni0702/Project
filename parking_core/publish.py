"""Build the static grid file the app downloads whole (D-011).

The file holds aggregates only: no events, no contributor ids, no coordinates.
"""
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from . import grid, slots
from .model import Outcome, estimate
from .privacy import Admission, class_value

MODEL_VERSION = "beta-binomial-0.1"


def build_grid(config: dict, outcomes: list[Outcome], now: datetime | None = None,
               previous_levels: dict[str, str] | None = None,
               admission: Admission | None = None) -> dict:
    """`admission` carries server-side state between publications (C6)."""
    admission = admission or Admission.from_config(config)
    now = now or datetime.now(ZoneInfo(config["timezone"]))
    outcomes = admission.filter(outcomes, now)
    slot = slots.slot_key(now, config["time"]["slot_minutes"])
    cells = grid.cells_for_bbox(config["grid"]["bbox"], config["grid"]["h3_resolution"])
    estimates = estimate(cells, slot, outcomes, config, grid.neighbors, previous_levels=previous_levels)
    return {
        "city": config["id"],
        "generated_at": now.isoformat(timespec="seconds"),
        "valid_minutes": config["publish"]["interval_minutes"],
        "slot": list(slot),
        "model_version": MODEL_VERSION,
        "h3_resolution": config["grid"]["h3_resolution"],
        "vehicle_odds": config["vehicles"]["odds"],  # applied on the device
        # cell -> [class value, level, reliability, based on user data]. No counts (C6).
        "cells": {
            cell: [class_value(e.level, config["display"]["class_values"]), e.level, e.reliability, e.from_user_data]
            for cell, e in estimates.items()
        },
    }


def write_grid(payload: dict, out_dir: Path) -> Path:
    path = out_dir / payload["city"] / "grid.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, separators=(",", ":")), encoding="utf-8")
    return path


def build_forecast(config: dict, outcomes: list[Outcome], now: datetime | None = None,
                   admission: Admission | None = None) -> dict:
    """Estimates for every day type and slot, without the "now" component (D-022).

    Only cells that differ from the prior-only estimate are listed: the app
    falls back to `default` for the others. No counts, no contributor ids.
    """
    admission = admission or Admission.from_config(config)
    now = now or datetime.now(ZoneInfo(config["timezone"]))
    outcomes = admission.filter(outcomes, now)
    cells = grid.cells_for_bbox(config["grid"]["bbox"], config["grid"]["h3_resolution"])
    no_live = {**config, "model": {**config["model"], "live_window_minutes": -1}}
    values = config["display"]["class_values"]
    slots_per_day = 1440 // config["time"]["slot_minutes"]

    def pack(e):
        return [class_value(e.level, values), e.level, e.reliability, e.from_user_data]

    default = pack(next(iter(estimate(cells[:1], ("weekday", 0), [], no_live, lambda c: []).values())))
    by_slot: dict[str, dict] = {}
    for day_type in config["time"]["day_types"]:
        for index in range(slots_per_day):
            slot = (day_type, index)
            mine = [o for o in outcomes if o.slot == slot]
            if not mine:
                continue
            est = estimate(cells, slot, outcomes, no_live, grid.neighbors)
            diff = {c: pack(e) for c, e in est.items() if pack(e) != default}
            if diff:
                by_slot.setdefault(day_type, {})[str(index)] = diff
    return {
        "city": config["id"],
        "generated_at": now.isoformat(timespec="seconds"),
        "model_version": MODEL_VERSION,
        "h3_resolution": config["grid"]["h3_resolution"],
        "slot_minutes": config["time"]["slot_minutes"],
        "vehicle_odds": config["vehicles"]["odds"],
        "default": default,
        "slots": by_slot,
    }


def write_forecast(payload: dict, out_dir: Path) -> Path:
    path = out_dir / payload["city"] / "forecast.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, separators=(",", ":")), encoding="utf-8")
    return path
