from typing import Optional

from datetime import date


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


def filter_range(events: list[Event], start: Optional[date], end: Optional[date]):
    if start is None and end is None:
        return events

    elif start is not None and end is None:
        return list(filter(lambda event: start == event.canonical_date, events))

    elif start is not None and end is not None:
        return filter(lambda event: start <= event.canonical_date <= end, events)

    else:
        raise Exception()
