"""Event store behind a small interface, so SQLite can be swapped for PostgreSQL.

Privacy (C5, C7): no arrival time, no IP, no user agent. Only the calendar day
(for retention) and the declared slot are stored.
"""
import sqlite3
from contextlib import closing
from datetime import date, timedelta
from typing import Protocol

SCHEMA = """
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    cell TEXT NOT NULL,
    day_type TEXT NOT NULL,
    slot_index INTEGER NOT NULL,
    search_bucket INTEGER,
    vehicle_class TEXT,
    pid TEXT NOT NULL,
    app_version TEXT NOT NULL,
    day TEXT NOT NULL,
    UNIQUE (pid, type, cell, day)
);
CREATE INDEX IF NOT EXISTS events_day ON events (day);
CREATE TABLE IF NOT EXISTS admitted (
    cell TEXT NOT NULL,
    pid TEXT NOT NULL,
    day TEXT NOT NULL,
    PRIMARY KEY (cell, pid)
);
"""


class EventStore(Protocol):
    def add_event(self, event: dict, day: date) -> bool:
        """Insert; False when the per-day rate limit (C9) rejects it."""

    def events(self) -> list[dict]: ...
    def delete_older_than(self, cutoff: date) -> int: ...
    def load_admitted(self) -> dict[str, set[str]]: ...
    def save_admitted(self, admitted: dict[str, set[str]], day: date) -> None: ...


class SqliteStore:
    def __init__(self, path: str):
        self.path = path
        if path != ":memory:":
            import os
            os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        self._keep = sqlite3.connect(path, check_same_thread=False) if path == ":memory:" else None
        with closing(self._connect()) as db:
            db.executescript(SCHEMA)
            db.commit()

    def _connect(self) -> sqlite3.Connection:
        if self._keep is not None:  # in-memory db must stay on one connection
            return _Shared(self._keep)
        db = sqlite3.connect(self.path)
        db.row_factory = sqlite3.Row
        return db

    def add_event(self, event: dict, day: date) -> bool:
        with closing(self._connect()) as db:
            try:
                db.execute(
                    "INSERT INTO events (type, cell, day_type, slot_index, search_bucket,"
                    " vehicle_class, pid, app_version, day) VALUES (?,?,?,?,?,?,?,?,?)",
                    (event["type"], event["cell"], event["slot_day_type"], event["slot_index"],
                     event.get("search_bucket"), event.get("vehicle_class"), event["pid"],
                     event["app_version"], day.isoformat()),
                )
                db.commit()
                return True
            except sqlite3.IntegrityError:
                return False

    def events(self) -> list[dict]:
        with closing(self._connect()) as db:
            return [dict(r) for r in db.execute("SELECT * FROM events")]

    def delete_older_than(self, cutoff: date) -> int:
        with closing(self._connect()) as db:
            n = db.execute("DELETE FROM events WHERE day < ?", (cutoff.isoformat(),)).rowcount
            db.execute("DELETE FROM admitted WHERE day < ?", (cutoff.isoformat(),))
            db.commit()
            return n

    def load_admitted(self) -> dict[str, set[str]]:
        result: dict[str, set[str]] = {}
        with closing(self._connect()) as db:
            for row in db.execute("SELECT cell, pid FROM admitted"):
                result.setdefault(row["cell"], set()).add(row["pid"])
        return result

    def save_admitted(self, admitted: dict[str, set[str]], day: date) -> None:
        with closing(self._connect()) as db:
            db.executemany(
                "INSERT OR IGNORE INTO admitted (cell, pid, day) VALUES (?,?,?)",
                [(c, p, day.isoformat()) for c, ids in admitted.items() for p in ids],
            )
            db.commit()


class _Shared:
    """Wrap the shared in-memory connection so `closing()` does not close it."""

    def __init__(self, db: sqlite3.Connection):
        self._db = db
        db.row_factory = sqlite3.Row

    def __getattr__(self, name):
        return getattr(self._db, name)

    def close(self):
        pass


def retention_cutoff(today: date, days: int) -> date:
    return today - timedelta(days=days)
