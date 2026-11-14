"""Time slots: (day type, slot index). Holidays come from the city pipeline."""
from datetime import date, datetime


def day_type(day: date, holidays: frozenset[date] = frozenset()) -> str:
    if day in holidays or day.weekday() == 6:
        return "holiday"
    return "saturday" if day.weekday() == 5 else "weekday"


def slot_key(local_time: datetime, slot_minutes: int, holidays: frozenset[date] = frozenset()) -> tuple[str, int]:
    index = (local_time.hour * 60 + local_time.minute) // slot_minutes
    return day_type(local_time.date(), holidays), index
