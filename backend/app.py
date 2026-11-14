"""FastAPI app. One deployment serves one city, chosen by configuration."""
import os
import re
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from zoneinfo import ZoneInfo

import h3
from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import FileResponse

from parking_core import grid
from parking_core.config import load_city

from .schemas import EventIn
from .store import SqliteStore, retention_cutoff

ROOT = Path(__file__).resolve().parent.parent
CITY_ID = re.compile(r"^[a-z0-9_-]{1,40}$")


def create_app(city_id: str | None = None, db_path: str | None = None,
               out_dir: Path | None = None, store=None) -> FastAPI:
    city_id = city_id or os.environ["PARKING_CITY"]
    config = load_city(city_id)
    store = store or SqliteStore(db_path or os.environ.get("PARKING_DB", str(ROOT / "data/backend/events.sqlite3")))
    out_dir = out_dir or Path(os.environ.get("PARKING_OUT", ROOT / "build/grid"))
    tz = ZoneInfo(config["timezone"])
    resolution = config["grid"]["h3_resolution"]
    day_types = set(config["time"]["day_types"])
    slots_per_day = 1440 // config["time"]["slot_minutes"]

    @lru_cache(maxsize=1)
    def city_cells() -> frozenset[str]:
        return frozenset(grid.cells_for_bbox(config["grid"]["bbox"], resolution))

    app = FastAPI(title="parking backend", docs_url=None, redoc_url=None, openapi_url=None)
    app.state.store, app.state.config, app.state.out_dir = store, config, out_dir

    @app.post("/v1/events", status_code=202)
    def post_event(event: EventIn):
        if not (h3.is_valid_cell(event.cell) and h3.get_resolution(event.cell) == resolution
                and event.cell in city_cells()):
            raise HTTPException(422, "cell outside the city grid")
        if event.slot_day_type not in day_types or event.slot_index >= slots_per_day:
            raise HTTPException(422, "invalid slot")
        today = datetime.now(tz).date()  # only the day is kept, never the arrival time (C7)
        if not store.add_event(event.model_dump(), today):
            raise HTTPException(429, "rate limit")  # C9 defence: 1 per type and cell per day
        return Response(status_code=202)

    def _serve(city: str, name: str):
        path = out_dir / city / name
        if not CITY_ID.match(city) or not path.is_file():
            raise HTTPException(404)
        return FileResponse(path, media_type="application/json")

    @app.get("/v1/grid/{city}")
    def get_grid(city: str):
        return _serve(city, "grid.json")

    @app.get("/v1/forecast/{city}")
    def get_forecast(city: str):
        return _serve(city, "forecast.json")

    return app


def run_retention(store, config: dict, today=None) -> int:
    today = today or datetime.now(ZoneInfo(config["timezone"])).date()
    return store.delete_older_than(retention_cutoff(today, config["privacy"]["raw_retention_days"]))
