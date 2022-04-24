from datetime import date
from enum import Enum
from typing import Optional

import pytz
from api.datatype.Event import Event, filter_range
from api.datatype.WaitTimesDay import WaitTimesDay
from eatery.datatype.EateryAlert import EateryAlert


class EateryID(Enum):
    ONE_ZERO_FOUR_WEST = 1
    LIBE_CAFE = 2
    ATRIUM_CAFE = 3
    BEAR_NECESSITIES = 4
    BECKER_HOUSE = 5
    BIG_RED_BARN = 6
    BUS_STOP_BAGELS = 7
    CAFE_JENNIE = 8
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
    MORRISON_DINING = 39
    NULL_EATERY = 41


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
        payment_accepts_cash: Optional[bool] = None,
        payment_accepts_brbs: Optional[bool] = None,
        payment_accepts_meal_swipes: Optional[bool] = None,
        location: Optional[str] = None,
        online_order_url: Optional[str] = None,
        wait_times: Optional[list[WaitTimesDay]] = None,
        alerts: Optional[list[EateryAlert]] = None,
    ):
        self.id = id
        self.name = name
        self.image_url = image_url
        self.menu_summary = menu_summary
        self.campus_area = campus_area
        self.latitude = latitude
        self.longitude = longitude
        self.known_events = events
        self.payment_accepts_cash = payment_accepts_cash
        self.payment_accepts_brbs = payment_accepts_brbs
        self.payment_accepts_meal_swipes = payment_accepts_meal_swipes
        self.location = location
        self.online_order_url = online_order_url
        self.wait_times = wait_times
        self.alerts = alerts

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
        end: Optional[date] = None,
    ):
        eatery = {
            "id": None if self.id is None else self.id.value,
            "name": self.name,
            "image_url": self.image_url,
            "menu_summary": self.menu_summary,
            "campus_area": self.campus_area,
            "events": None
            if self.known_events is None
            else [event.to_json() for event in self.events(tzinfo, start, end)],
            "latitude": self.latitude,
            "longitude": self.longitude,
            "payment_accepts_cash": self.payment_accepts_cash,
            "payment_accepts_brbs": self.payment_accepts_brbs,
            "payment_accepts_meal_swipes": self.payment_accepts_meal_swipes,
            "location": self.location,
            "online_order_url": self.online_order_url,
            "wait_times": None
            if self.wait_times is None
            else [wait_time.to_json() for wait_time in self.wait_times],
            "alerts": None
            if self.alerts is None
            else [alert.to_json() for alert in self.alerts],
        }
        return eatery

    @staticmethod
    def from_json(eatery_json):
        return Eatery(
            id=None
            if "id" not in eatery_json or eatery_json["id"] is None
            else EateryID(eatery_json["id"]),
            name=eatery_json.get("name"),
            image_url=eatery_json.get("image_url"),
            menu_summary=eatery_json.get("menu_summary"),
            campus_area=eatery_json.get("campus_area"),
            events=None
            if "events" not in eatery_json or eatery_json["events"] is None
            else [Event.from_json(event) for event in eatery_json["events"]],
            latitude=eatery_json.get("latitude"),
            longitude=eatery_json.get("longitude"),
            payment_accepts_cash=eatery_json.get("payment_accepts_cash"),
            payment_accepts_brbs=eatery_json.get("payment_accepts_brbs"),
            payment_accepts_meal_swipes=eatery_json.get("payment_accepts_meal_swipes"),
            location=eatery_json.get("location"),
            online_order_url=eatery_json.get("online_order_url"),
            wait_times=None
            if "wait_times" not in eatery_json or eatery_json["wait_times"] is None
            else [
                WaitTimesDay.from_json(day_wait_time)
                for day_wait_time in eatery_json["wait_times"]
            ],
            alerts=None
            if "alerts" not in eatery_json or eatery_json["alerts"] is None
            else [EateryAlert.from_json(alert) for alert in eatery_json["alerts"]],
        )

    def clone(self):
        return Eatery.from_json(self.to_json())