from typing import Optional
from datetime import date, time, datetime
from api.datatype.Menu import Menu

import pytz


class Event:

    def __init__(
            self,
            description: str,
            canonical_date: date,
            start_timestamp: int,
            end_timestamp: int,
            menu: Menu
    ):
        self.description = description
        self.canonical_date = canonical_date
        self.start_timestamp = start_timestamp
        self.end_timestamp = end_timestamp
        self.menu = menu

    def to_json(
        self,
        tzinfo: Optional[pytz.timezone] = None,
        start: Optional[date] = None,
        end: Optional[date] = None
    ):
        return {
            "description": self.description,
            "canonical_date": str(self.canonical_date),
            "start_timestamp": self.start_timestamp,
            "end_timestamp": self.end_timestamp,
            "menu": self.menu.to_json()
        }

    @staticmethod
    def from_json(event_json):
        return Event(
            description=event_json["description"],
            canonical_date=date.fromisoformat(event_json["canonical_date"]),
            start_timestamp=event_json["start_timestamp"],
            end_timestamp=event_json["end_timestamp"],
            menu=Menu.from_json(event_json["menu"])
        )

    def __contains__(self, item: int):
        return self.start_timestamp <= item <= self.end_timestamp

    #TODO: Restructure to move to some util file into major folder outside of api
    @staticmethod
    def combined_timestamp(date: date, time: time, tzinfo: pytz.timezone) -> int:
        """
            Returns the Unix (UTC) timestamp of the combined (date, time) in the
            New York timezone.
        """
        return int(tzinfo.localize(datetime.combine(date, time)).timestamp())


def filter_range(events: list[Event], tzinfo: Optional[pytz.timezone], start: Optional[date], end: Optional[date]):
    if events is None:
        return []

    if start is None and end is None:
        return events

    elif tzinfo is not None and start is not None and end is None:
        start_ts = Event.combined_timestamp(start, time(), tzinfo)
        return [event for event in events if (
                (start_ts in event) or start == event.canonical_date
        )]

    elif tzinfo is not None and start is not None and end is not None:
        start_ts = Event.combined_timestamp(start, time(), tzinfo)
        end_ts = Event.combined_timestamp(end, time(), tzinfo)
        return [event for event in events if (
                (start_ts in event) or (end_ts in event) or start <= event.canonical_date <= end
        )]

    else:
        raise Exception(f"Improper arguments. tzinfo={tzinfo}, start={start}, end={end}")