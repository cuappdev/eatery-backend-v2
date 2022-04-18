from datetime import date, time
from typing import Optional

import pytz
from api.datatype.Menu import Menu
from api.util.time import combined_timestamp


class Event:
    """
    Represents an event on a particular date

    Attributes
    ----------
    description
        the event description
    canonical date
        the date on which the event started
    start_timestamp
        timestamp of the exact time the event started
    end_timestamp
        timestamp of the exact time the event ended
    menu
        the menu associated with the event
    generated_by
        id of repeating schedule that generated this event (if exists)
    """

    def __init__(
        self,
        description: str,
        canonical_date: date,
        start_timestamp: int,
        end_timestamp: int,
        menu: Menu,
        generated_by: Optional[int] = None,
    ):
        self.description = description
        self.canonical_date = canonical_date
        self.start_timestamp = start_timestamp
        self.end_timestamp = end_timestamp
        self.menu = menu
        self.generated_by = generated_by

    def to_json(
        self,
        tzinfo: Optional[pytz.timezone] = None,
        start: Optional[date] = None,
        end: Optional[date] = None,
    ):
        return {
            "description": self.description,
            "canonical_date": str(self.canonical_date),
            "start_timestamp": self.start_timestamp,
            "end_timestamp": self.end_timestamp,
            "menu": self.menu.to_json() if self.menu else None,
            "generated_by": self.generated_by,
        }

    @staticmethod
    def from_json(event_json):
        return Event(
            description=event_json["description"],
            canonical_date=date.fromisoformat(event_json["canonical_date"]),
            start_timestamp=event_json["start_timestamp"],
            end_timestamp=event_json["end_timestamp"],
            menu=Menu.from_json(event_json["menu"]),
            generated_by=event_json.get("generated_by"),
        )

    def __contains__(self, item: int):
        return self.start_timestamp <= item <= self.end_timestamp


def filter_range(
    events: list[Event],
    tzinfo: Optional[pytz.timezone],
    start: Optional[date],
    end: Optional[date],
):
    """
    Filters a list of events based on the parameters provided.
    If neither start nor end is provided no filtering occurs.
    If tzinfo and start are provided, returns a new list containing all events that start on start
    If all 3 optional parameters are provided, returns a new list containing all events
    between start and end
    """
    if events is None:
        return []

    if start is None and end is None:
        return events

    elif tzinfo is not None and start is not None and end is None:
        start_ts = combined_timestamp(start, time(), tzinfo)
        return [
            event
            for event in events
            if ((start_ts in event) or start == event.canonical_date)
        ]

    elif tzinfo is not None and start is not None and end is not None:
        start_ts = combined_timestamp(start, time(), tzinfo)
        end_ts = combined_timestamp(end, time(), tzinfo)
        return [
            event
            for event in events
            if (
                (start_ts in event)
                or (end_ts in event)
                or start <= event.canonical_date <= end
            )
        ]

    else:
        raise Exception(
            f"Improper arguments. tzinfo={tzinfo}, start={start}, end={end}"
        )
