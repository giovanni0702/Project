"""Strict event contract: anything not listed here is rejected with 422 (C5).

Every field has a written justification (T-040):
  type          always "parked": departures are not collected (no use in the model; attack 5).
                Kept so the pseudonym (which includes the type) and the server agree.
  cell          H3 cell of the parking (the only place information).
  slot_*        declared time slot: needed for the per-slot estimate.
  search_bucket outcome of the search (0-3): the quantity being estimated.
  vehicle_class optional; counted in city-wide counters and discarded, never stored with the event.
  pid           per-cell pseudonym (C1), needed to count distinct people (k).
  app_version   used to reject incompatible clients; validated and discarded, never stored.
"""
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class EventIn(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    type: Literal["parked"]
    cell: str
    slot_day_type: str
    slot_index: int = Field(ge=0)
    search_bucket: Literal[0, 1, 2, 3]  # 0-2 / 2-5 / 5-10 / 10+ min
    vehicle_class: Literal["moto", "small", "medium", "large"] | None = None
    pid: str = Field(pattern=r"^[0-9a-f]{20}$")
    app_version: str = Field(pattern=r"^\d{1,3}(\.\d{1,3}){0,2}$", max_length=20)
