from datetime import date
from typing import Optional

import pytz

from api.dfg.preparation.datatype.OverrideEvent import OverrideEvent, filter_range

class OverrideEatery:

    def __init__(
            self,
            name: str,
            about: Optional[str] = None,
            campus_area: Optional[str] = None,
            latitude: Optional[float] = None,
            longitude: Optional[float] = None,
            events: Optional[list[OverrideEvent]] = None,
            payment_methods: Optional[list[str]] = None,
            location: Optional[str] = None,
            online_order: Optional[bool] = None,
            online_order_url: Optional[str] = None
    ):
        self.name = name
        self.about = about
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

