"""Privacy mechanisms required by the DPIA draft (docs/15-dpia-bozza.md, C1-C12).

Kept in the core so the device code, the server and the re-identification
test all use the same implementation.
"""
import hashlib
import hmac

EPOCH_DAYS = 28


def pseudonym(device_secret: bytes, event_type: str, cell: str, day_number: int) -> str:
    """C1: per-cell pseudonym. The server cannot link events of different cells,
    nor a parking event to a departure, nor one 28-day epoch to the next."""
    message = f"{event_type}|{cell}|{day_number // EPOCH_DAYS}".encode()
    return hmac.new(device_secret, message, hashlib.sha256).hexdigest()[:20]


class Admission:
    """C6, anti-differencing: new contributors enter the published estimate only
    in batches of at least `batch` distinct pseudonyms per cell, so no change
    between two consecutive grids can be attributed to a single person.

    `admitted` is server-side state and is never published.
    """

    def __init__(self, batch: int = 2, admitted: dict[str, set[str]] | None = None):
        self.batch = batch
        self.admitted = admitted or {}

    def filter(self, outcomes: list) -> list:
        pending: dict[str, set[str]] = {}
        for o in outcomes:
            if o.contributor not in self.admitted.get(o.cell, ()):
                pending.setdefault(o.cell, set()).add(o.contributor)
        for cell, ids in pending.items():
            if len(ids) >= self.batch:
                self.admitted.setdefault(cell, set()).update(ids)
        return [o for o in outcomes if o.contributor in self.admitted.get(o.cell, ())]


def class_value(level: str, representatives: dict[str, float]) -> float:
    """C6: publish a class representative, never the exact probability or counts."""
    return representatives[level]
