from typing import Optional

from datetime import date, datetime, time

import pytz


class Event:

    def __init__(
            self,
            canonical_date: date,
            start_timestamp: int,
            end_timestamp: int,
    ):
        self.canonical_date = canonical_date
        self.start_timestamp = start_timestamp
        self.end_timestamp = end_timestamp

    def to_json(self):
        raise Exception()

    def __contains__(self, item: int):
        return self.start_timestamp <= item <= self.end_timestamp


def _combined_timestamp(date: date, time: time, tzinfo: pytz.timezone) -> int:
    return int(tzinfo.localize(datetime.combine(date, time)).timestamp())


def filter_range(events: list[Event], tzinfo: Optional[pytz.timezone], start: Optional[date], end: Optional[date]):
    if start is None and end is None:
        return events

    elif tzinfo is not None and start is not None and end is None:
        start_ts = _combined_timestamp(start, time(), tzinfo)
        return [event for event in events if (
                (start_ts in event) or start == event.canonical_date
        )]

    elif tzinfo is not None and start is not None and end is not None:
        start_ts = _combined_timestamp(start, time(), tzinfo)
        end_ts = _combined_timestamp(end, time(), tzinfo)
        return [event for event in events if (
                (start_ts in event) or (end_ts in event) or start <= event.canonical_date <= end
        )]

    else:
        raise Exception(f"Improper arguments. tzinfo={tzinfo}, start={start}, end={end}")
