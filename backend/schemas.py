"""Strict event contract: anything not listed here is rejected with 422 (C5)."""
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class EventIn(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)

    type: Literal["parked", "left"]
    cell: str
    slot_day_type: str
    slot_index: int = Field(ge=0)
    search_bucket: Literal[0, 1, 2, 3] | None = None  # 0-2 / 2-5 / 5-10 / 10+ min
    vehicle_class: Literal["moto", "small", "medium", "large"] | None = None
    pid: str = Field(pattern=r"^[0-9a-f]{20}$")
    app_version: str = Field(pattern=r"^\d{1,3}(\.\d{1,3}){0,2}$", max_length=20)

    @model_validator(mode="after")
    def _bucket_only_for_parked(self):
        if self.type == "parked" and self.search_bucket is None:
            raise ValueError("search_bucket is required for 'parked'")
        if self.type == "left" and self.search_bucket is not None:
            raise ValueError("search_bucket is only allowed for 'parked'")
        return self
