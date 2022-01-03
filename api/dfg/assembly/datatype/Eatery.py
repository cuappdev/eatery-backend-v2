from datetime import date
from typing import Optional

import pytz

from api.dfg.preparation.datatype.Event import Event, filter_range

class Eatery:

    def __init__(
            self,
            id: int,
            name: str,
            campus_area: str,
            events: list[Event],
            latitude: float,
            longitude: float,
            payment_methods: list[str],
            location: str,
            online_order: bool,
            online_order_url: str
    ):
        self.id = id
        self.name = name
        self.campus_area = campus_area
        self.latitude = latitude
        self.longitude = longitude
        self.known_events = events
        self.payment_methods = payment_methods
        self.location = location
        self.online_order = online_order
        self.online_order_url = online_order_url

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
        eatery = {
            "id": self.id,
            "name": self.name,
            "campus_area": self.campus_area,
            "events": [event.to_json() for event in self.events(tzinfo, start, end)],
            "latitude": self.latitude,
            "longitude": self.longitude,
            "payment_methods": None if self.payment_methods is None else [payment_method for payment_method in self.payment_methods],
            "location": self.location,
            "online_order": self.online_order,
            "online_order_url": self.online_order_url
        }
        return eatery

