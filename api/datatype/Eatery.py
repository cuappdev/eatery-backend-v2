from datetime import date
from typing import Optional
from enum import Enum

import pytz
from api.datatype.EateryException import EateryException

from api.datatype.Event import Event, filter_range
from api.datatype.WaitTimesDay import WaitTimesDay


class EateryID(Enum):
    ONE_ZERO_FOUR_WEST = 1
    LIBE_CAFE = 2
    ATRIUM_CAFE = 3
    BEAR_NECESSITIES = 4
    BECKER_HOUSE = 5
    BIG_RED_BARN = 6
    BUS_STOP_BAGELS = 7
    CAFE_JENNIE = 8
    CAROLS_CAFE = 9
    COOK_HOUSE = 10
    DAIRY_BAR = 11
    CROSSINGS_CAFE = 12
    FRANNYS = 13
    GOLDIES_CAFE = 14
    GREEN_DRAGON = 15
    HOT_DOG_CART = 16
    ICE_CREAM_BIKE = 17
    BETHE_HOUSE = 18
    JANSENS_MARKET = 19
    KEETON_HOUSE = 20
    MANN_CAFE = 21
    MARTHAS_CAFE = 22
    MATTINS_CAFE = 23
    MCCORMICKS = 24
    NORTH_STAR_DINING = 25
    OKENSHIELDS = 26
    RISLEY = 27
    RPCC = 28
    ROSE_HOUSE = 29
    RUSTYS = 30
    STRAIGHT_FROM_THE_MARKET = 31
    TRILLIUM = 32
    TERRACE = 33
    MACS_CAFE = 34
    TEMPLE_OF_ZEUS = 35
    GIMME_COFFEE = 36
    LOUIES = 37
    ANABELS_GROCERY = 38

class Eatery:

    def __init__(
            self,
            id: EateryID,
            name: Optional[str] = None,
            image_url: Optional[str] = None,
            menu_summary: Optional[str] = None,
            campus_area: Optional[str] = None,
            events: Optional[list[Event]] = None,
            latitude: Optional[float] = None,
            longitude: Optional[float] = None,
            payment_methods: Optional[list[str]] = None,
            location: Optional[str] = None,
            online_order: Optional[bool] = None,
            online_order_url: Optional[str] = None,
            wait_times: Optional[list[WaitTimesDay]] = None,
            exceptions: Optional[list[EateryException]] = None
    ):
        self.id = id
        self.name = name
        self.image_url = image_url
        self.menu_summary = menu_summary
        self.campus_area = campus_area
        self.latitude = latitude
        self.longitude = longitude
        self.known_events = events
        self.payment_methods = payment_methods
        self.location = location
        self.online_order = online_order
        self.online_order_url = online_order_url
        self.wait_times = wait_times
        self.exceptions = exceptions

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
            "id": self.id.value,
            "name": self.name,
            "image_url": self.image_url,
            "menu_summary": self.menu_summary,
            "campus_area": self.campus_area,
            "events": None if self.known_events is None
            else [event.to_json() for event in self.events(tzinfo, start, end)],
            "latitude": self.latitude,
            "longitude": self.longitude,
            "payment_methods": None if self.payment_methods is None
            else [payment_method for payment_method in self.payment_methods],
            "location": self.location,
            "online_order": self.online_order,
            "online_order_url": self.online_order_url,
            "wait_times": None if self.wait_times is None else [wait_time.to_json() for wait_time in self.wait_times],
            "exceptions": None if self.exceptions is None else [exception.to_json() for exception in self.exceptions]
        }
        return eatery

    @staticmethod 
    def parse_field(json, key):
        return None if key not in json else json[key]

    @staticmethod
    def from_json(eatery_json):
        return Eatery(
            id=None if "id" not in eatery_json else EateryID(eatery_json["id"]),
            name=Eatery.parse_field(eatery_json, "name"),
            image_url=Eatery.parse_field(eatery_json, "image_url"),
            menu_summary=Eatery.parse_field(eatery_json, "menu_summary"),
            campus_area=Eatery.parse_field(eatery_json, "campus_area"),
            events=None if "events" not in eatery_json or eatery_json["events"] is None
            else [Event.from_json(event) for event in eatery_json["events"]],
            latitude=Eatery.parse_field(eatery_json, "latitude"),
            longitude=Eatery.parse_field(eatery_json, "longitude"),
            payment_methods=Eatery.parse_field(eatery_json, "payment_methods"),
            location=Eatery.parse_field(eatery_json, "location"),
            online_order=Eatery.parse_field(eatery_json, "online_order"),
            online_order_url=Eatery.parse_field(eatery_json, "online_order_url"),
            wait_times=None if "wait_times" not in eatery_json or eatery_json["wait_times"] is None
            else [WaitTimesDay.from_json(day_wait_time) for day_wait_time in eatery_json["wait_times"]],
            exceptions=None if "exceptions" not in eatery_json or eatery_json["exceptions"] is None
            else [EateryException.from_json(exception) for exception in eatery_json["exceptions"]]
        )

    def clone(self):
        return Eatery.from_json(self.to_json())
