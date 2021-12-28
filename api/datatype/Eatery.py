from datetime import date
from typing import Mapping, Optional
from .WaitTime import WaitTime

import pytz

from api.datatype.Event import Event, filter_range

class Eatery:

    def __init__(
            self,
            name: str,
            campus_area: str,
            events: list[Event],
            latitude: float,
            longitude: float
    ):
        self.name = name
        self.campus_area = campus_area
        self.latitude = latitude
        self.longitude = longitude
        self.known_events = events

    def events(
            self,
            tzinfo: Optional[pytz.timezone] = None,
            start: Optional[date] = None,
            end: Optional[date] = None,
    ):
        return filter_range(self.known_events, tzinfo, start, end)

    def to_json(
            self,
            tzinfo: Optional[pytz.timezone] = None,
            start: Optional[date] = None,
            end: Optional[date] = None
    ):
        return {
            "campus_area": self.campus_area,
            "events": [event.to_json() for event in self.events(tzinfo, start, end)],
            "latitude": self.latitude,
            "longitude": self.longitude,
            "name": self.name,
        }

