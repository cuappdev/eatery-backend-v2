from datetime import date
from typing import Optional

import pytz

from api.dfg.preparation.datatype.Event import Event, filter_range

class CornellDiningEatery:

    def __init__(
            self,
            name: str,
            about: str,
            about_short: str,
            campus_area: str,
            events: list[Event],
            latitude: float,
            longitude: float,
            payment_methods: list[str],
            location: str,
            online_order: bool,
            online_order_url: str
    ):
        self.name = name
        self.about = about
        self.about_short = about_short
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
            "name": self.name,
            "about": self.about,
            "about_short": self.about_short,
            "campus_area": self.campus_area,
            "events": [event.to_json() for event in self.events(tzinfo, start, end)],
            "latitude": self.latitude,
            "longitude": self.longitude,
            "payment_methods": [payment_method for payment_method in self.payment_methods],
            "location": self.location,
            "online_order": self.online_order,
            "online_order_url": self.online_order_url
        }
        return eatery

