"""Build the static grid file the app downloads whole (D-011).

The file holds aggregates only: no events, no contributor ids, no coordinates.
"""
import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from . import grid, slots
from .model import Outcome, estimate

MODEL_VERSION = "beta-binomial-0.1"


def build_grid(config: dict, outcomes: list[Outcome], now: datetime | None = None,
               previous_levels: dict[str, str] | None = None) -> dict:
    now = now or datetime.now(ZoneInfo(config["timezone"]))
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
        # cell -> [probability, level, reliability, based on user data]
        "cells": {
            cell: [round(e.probability, 2), e.level, e.reliability, e.from_user_data]
            for cell, e in estimates.items()
        },
    }


def write_grid(payload: dict, out_dir: Path) -> Path:
    path = out_dir / payload["city"] / "grid.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, separators=(",", ":")), encoding="utf-8")
    return path
