"""Privacy mechanisms required by the DPIA draft (docs/15-dpia-bozza.md, C1-C12).

Kept in the core so the device code, the server and the re-identification
test all use the same implementation.
"""
import hashlib
import hmac
import re
from collections import Counter

EPOCH_DAYS = 28
_EPOCH_TAG = re.compile(r"[0-9a-f]{4}")


def pseudonym(device_secret: bytes, event_type: str, cell: str, day_number: int) -> str:
    """C1: per-cell pseudonym. The server cannot link events of different cells,
    nor a parking event to a departure, nor one 28-day epoch to the next.

    Layout: 4 hex digits of epoch number (public: it is a function of the date,
    the server learns nothing new) + 16 hex digits of HMAC. The tag lets the
    server count k on pseudonyms of one epoch only (T-040, attack 6)."""
    epoch = day_number // EPOCH_DAYS
    message = f"{event_type}|{cell}|{epoch}".encode()
    digest = hmac.new(device_secret, message, hashlib.sha256).hexdigest()[:16]
    return f"{epoch % 65536:04x}{digest}"


def pid_epoch(pid: str) -> int:
    """Epoch tag of a pseudonym (0 for ids that carry none, e.g. test labels)."""
    head = pid[:4]
    return int(head, 16) if _EPOCH_TAG.fullmatch(head) else 0


def people_lower_bound(pids) -> int:
    """C2: number of people guaranteed by a set of pseudonyms. Pseudonyms of
    different epochs may belong to the same person, so only pseudonyms of one
    epoch count as distinct: the largest same-epoch group is the safe bound."""
    per_epoch = Counter(pid_epoch(p) for p in set(pids))
    return max(per_epoch.values(), default=0)


class Admission:
    """C6, anti-differencing: new contributors enter the published estimate only
    in batches of at least `batch` people per cell, and only at fixed, wide
    intervals (`interval_minutes`, aligned to the clock), so a change between
    two grids neither comes from a single person nor reveals when a block arrived.

    `interval_minutes = 0` admits at every call (tests of the batch rule only).
    `admitted` is server-side state and is never published.
    """

    def __init__(self, batch: int = 2, admitted: dict[str, set[str]] | None = None,
                 interval_minutes: int = 0, step_minutes: int = 5):
        self.batch = batch
        self.admitted = {} if admitted is None else admitted
        self.interval = interval_minutes
        self.step = step_minutes

    @classmethod
    def from_config(cls, config: dict, admitted: dict[str, set[str]] | None = None) -> "Admission":
        privacy = config["privacy"]
        return cls(privacy["admission_batch"], admitted, privacy["admission_interval_minutes"],
                   config["publish"]["interval_minutes"])

    def window_open(self, now) -> bool:
        """True only in the first publication step of each interval. No clock: never open."""
        if self.interval <= 0:
            return True
        if now is None:
            return False
        return (now.hour * 60 + now.minute) % self.interval < self.step

    def filter(self, outcomes: list, now=None) -> list:
        if self.window_open(now):
            pending: dict[str, set[str]] = {}
            for o in outcomes:
                if o.contributor not in self.admitted.get(o.cell, ()):
                    pending.setdefault(o.cell, set()).add(o.contributor)
            for cell, ids in pending.items():
                if people_lower_bound(ids) >= self.batch:
                    self.admitted.setdefault(cell, set()).update(ids)
        return [o for o in outcomes if o.contributor in self.admitted.get(o.cell, ())]


def class_value(level: str, representatives: dict[str, float]) -> float:
    """C6: publish a class representative, never the exact probability or counts."""
    return representatives[level]
