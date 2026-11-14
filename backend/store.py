"""Event store behind a small interface, so SQLite can be swapped for PostgreSQL.

Privacy (C5, C7, T-040): the history keeps no arrival time, no IP, no user agent,
no app version, no vehicle class and no departures. Only the ISO week (Monday's date)
and the declared slot are kept per parking event. Short-lived side tables:
  live          event -> 5-minute step, deleted after the live window (feeds "now");
  daily_seen    (pid, cell, day) for the per-day rate limit (C9), deleted next day;
  vehicle_outcomes  (week, class, bucket, n): city-wide counters, no cell, pid or event link.
"""
import sqlite3
from contextlib import closing
from datetime import date, datetime, timedelta
from typing import Protocol

SCHEMA = """
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cell TEXT NOT NULL,
    day_type TEXT NOT NULL,
    slot_index INTEGER NOT NULL,
    search_bucket INTEGER NOT NULL,
    pid TEXT NOT NULL,
    week TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS events_week ON events (week);
CREATE TABLE IF NOT EXISTS live (
    event_id INTEGER PRIMARY KEY,
    step INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS daily_seen (
    pid TEXT NOT NULL,
    cell TEXT NOT NULL,
    day TEXT NOT NULL,
    PRIMARY KEY (pid, cell, day)
);
CREATE TABLE IF NOT EXISTS vehicle_outcomes (
    week TEXT NOT NULL,
    vehicle_class TEXT NOT NULL,
    search_bucket INTEGER NOT NULL,
    n INTEGER NOT NULL,
    PRIMARY KEY (week, vehicle_class, search_bucket)
);
CREATE TABLE IF NOT EXISTS admitted (
    cell TEXT NOT NULL,
    pid TEXT NOT NULL,
    week TEXT NOT NULL,
    PRIMARY KEY (cell, pid)
);
"""


def week_start(day: date) -> date:
    """Monday of the ISO week: the only date granularity kept in the history."""
    return day - timedelta(days=day.weekday())


def current_step(now: datetime, step_minutes: int) -> int:
    """Index of the publication step containing `now` (epoch minutes // step)."""
    return int(now.timestamp() // 60 // step_minutes)


def oldest_live_step(now: datetime, step_minutes: int, window_minutes: int) -> int:
    """Rows older than this step are past the live window and must be deleted."""
    return current_step(now, step_minutes) - -(-window_minutes // step_minutes)


class EventStore(Protocol):
    def add_event(self, event: dict, day: date, live_step: int | None = None) -> bool:
        """Insert a parking event; False when the per-day rate limit (C9) rejects it.
        Departures are not stored. `live_step` feeds the short-lived live table."""

    def events(self) -> list[dict]: ...
    def purge_live(self, oldest_step: int) -> int: ...
    def delete_older_than(self, cutoff: date) -> int: ...
    def load_admitted(self) -> dict[str, set[str]]: ...
    def save_admitted(self, admitted: dict[str, set[str]], day: date) -> None: ...
    def vehicle_totals(self) -> dict[tuple[str, int], int]: ...


class SqliteStore:
    def __init__(self, path: str):
        self.path = path
        if path != ":memory:":
            import os
            os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        self._keep = sqlite3.connect(path, check_same_thread=False) if path == ":memory:" else None
        with closing(self._connect()) as db:
            columns = {r[1] for r in db.execute("PRAGMA table_info(events)")}
            if columns & {"day", "vehicle_class", "app_version", "type"}:
                raise RuntimeError("legacy events schema (pre T-040): migrate or reset the database; "
                                   "deleting real user data is a founder decision")
            db.executescript(SCHEMA)
            db.commit()

    def _connect(self) -> sqlite3.Connection:
        if self._keep is not None:  # in-memory db must stay on one connection
            return _Shared(self._keep)
        db = sqlite3.connect(self.path)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA secure_delete=ON")  # deleted live rows are overwritten, not left in free pages
        return db

    def add_event(self, event: dict, day: date, live_step: int | None = None) -> bool:
        if event["type"] != "parked":
            return True  # departures carry no value for the model and are never stored (T-040, attack 5)
        with closing(self._connect()) as db:
            db.execute("DELETE FROM daily_seen WHERE day < ?", (day.isoformat(),))
            try:
                db.execute("INSERT INTO daily_seen (pid, cell, day) VALUES (?,?,?)",
                           (event["pid"], event["cell"], day.isoformat()))
            except sqlite3.IntegrityError:
                db.rollback()
                return False
            week = week_start(day).isoformat()
            cur = db.execute(
                "INSERT INTO events (cell, day_type, slot_index, search_bucket, pid, week) VALUES (?,?,?,?,?,?)",
                (event["cell"], event["slot_day_type"], event["slot_index"], event["search_bucket"],
                 event["pid"], week))
            if live_step is not None:
                db.execute("INSERT INTO live (event_id, step) VALUES (?,?)", (cur.lastrowid, live_step))
            if event.get("vehicle_class"):  # counted, never stored with the event (attack 4)
                db.execute(
                    "INSERT INTO vehicle_outcomes (week, vehicle_class, search_bucket, n) VALUES (?,?,?,1) "
                    "ON CONFLICT (week, vehicle_class, search_bucket) DO UPDATE SET n = n + 1",
                    (week, event["vehicle_class"], event["search_bucket"]))
            db.commit()
            return True

    def events(self) -> list[dict]:
        with closing(self._connect()) as db:
            return [dict(r) for r in db.execute(
                "SELECT e.cell, e.day_type, e.slot_index, e.search_bucket, e.pid, e.week, l.step AS live_step "
                "FROM events e LEFT JOIN live l ON l.event_id = e.id")]

    def purge_live(self, oldest_step: int) -> int:
        with closing(self._connect()) as db:
            n = db.execute("DELETE FROM live WHERE step < ?", (oldest_step,)).rowcount
            db.commit()
            return n

    def delete_older_than(self, cutoff: date) -> int:
        """Weeks starting before the cutoff go: the true date is somewhere in the week,
        so the effective retention is between (days - 6) and `days`, never above."""
        with closing(self._connect()) as db:
            n = db.execute("DELETE FROM events WHERE week < ?", (cutoff.isoformat(),)).rowcount
            db.execute("DELETE FROM live WHERE event_id NOT IN (SELECT id FROM events)")
            db.execute("DELETE FROM admitted WHERE week < ?", (cutoff.isoformat(),))
            db.execute("DELETE FROM daily_seen WHERE day < ?", (cutoff.isoformat(),))
            db.commit()
            return n

    def load_admitted(self) -> dict[str, set[str]]:
        result: dict[str, set[str]] = {}
        with closing(self._connect()) as db:
            for row in db.execute("SELECT cell, pid FROM admitted"):
                result.setdefault(row["cell"], set()).add(row["pid"])
        return result

    def save_admitted(self, admitted: dict[str, set[str]], day: date) -> None:
        week = week_start(day).isoformat()
        with closing(self._connect()) as db:
            db.executemany(
                "INSERT OR IGNORE INTO admitted (cell, pid, week) VALUES (?,?,?)",
                [(c, p, week) for c, ids in admitted.items() for p in ids],
            )
            db.commit()

    def vehicle_totals(self) -> dict[tuple[str, int], int]:
        """City-wide counts per (vehicle class, search bucket), summed over weeks."""
        with closing(self._connect()) as db:
            return {(r["vehicle_class"], r["search_bucket"]): r["n"] for r in db.execute(
                "SELECT vehicle_class, search_bucket, SUM(n) AS n FROM vehicle_outcomes GROUP BY 1, 2")}


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
