from typing import Union

from src.dfg.DfgNode import DfgNode
import requests
from src.datatype.DiningHall import DiningHall
from src.datatype.Cafe import Cafe
from src.datatype.CafeMenu import CafeMenu
from src.datatype.CafeEvent import CafeEvent
from src.datatype.MenuItem import MenuItem
from src.datatype.DiningHallEvent import DiningHallEvent
from src.datatype.DiningHallMenuCategory import DiningHallMenuCategory
from src.datatype.DiningHallMenu import DiningHallMenu
from datetime import date


class CornellDiningNow(DfgNode):

    CORNELL_DINING_URL = "https://now.dining.cornell.edu/api/1.0/dining/eateries.json"

    def __call__(self, *args, **kwargs) -> list[Union[Cafe, DiningHall]]:
        try:
            response = requests.get(CornellDiningNow.CORNELL_DINING_URL).json()

        except Exception as e:
            raise e

        if response["status"] == "success":
            json_eateries = response["data"]["eateries"]
            eateries = []
            for json_eatery in json_eateries:
                eateries.append(CornellDiningNow.parse_eatery(json_eatery))

            return eateries

        else:
            raise Exception(response["message"])

    @staticmethod
    def parse_eatery(json_eatery: dict) -> Union[Cafe, DiningHall]:
        is_cafe = "Cafe" in {
            eatery_type["descr"]
            for eatery_type in json_eatery["eateryTypes"]
        }

        if is_cafe:
            return CornellDiningNow.cafe_from_json(json_eatery)
        else:
            return CornellDiningNow.dining_hall_from_json(json_eatery)

    @staticmethod
    def cafe_from_json(json_eatery: dict) -> Cafe:
        return Cafe(
            name=json_eatery["name"],
            campus_area=json_eatery["campusArea"]["descrshort"],
            events=CornellDiningNow.cafe_event_from_json(
                json_eatery["operatingHours"]
            ),
            latitude=json_eatery["latitude"],
            longitude=json_eatery["longitude"],
            menu=CornellDiningNow.cafe_menu_from_json(
                json_eatery["diningItems"]
            )
        )

    @staticmethod
    def cafe_event_from_json(json_operating_hours: list) -> list[CafeEvent]:
        json_operating_hours = sorted(
            json_operating_hours,
            key=lambda json_date_events: json_date_events["date"]
        )
        events = []

        for json_date_events in json_operating_hours:
            for json_event in json_date_events["events"]:
                events.append(CafeEvent(
                    canonical_date=date.fromisoformat(json_date_events["date"]),
                    start_timestamp=json_event["startTimestamp"],
                    end_timestamp=json_event["endTimestamp"]
                ))

        return events

    @staticmethod
    def cafe_menu_from_json(json_dining_items: list) -> CafeMenu:
        items = []

        for json_dining_item in json_dining_items:
            items.append(MenuItem(
                healthy=json_dining_item["healthy"],
                name=json_dining_item["item"]
            ))

        return CafeMenu(items=items)

    @staticmethod
    def dining_hall_from_json(json_eatery: dict) -> DiningHall:
        return DiningHall(
            name=json_eatery["name"],
            campus_area=json_eatery["campusArea"]["descrshort"],
            events=CornellDiningNow.dining_hall_events_from_json(
                json_operating_hours=json_eatery["operatingHours"]
            ),
            latitude=json_eatery["latitude"],
            longitude=json_eatery["longitude"],
        )

    @staticmethod
    def dining_hall_events_from_json(json_operating_hours: list) -> list[DiningHallEvent]:
        json_operating_hours = sorted(
            json_operating_hours,
            key=lambda json_date_events: json_date_events["date"]
        )
        events = []

        for json_date_events in json_operating_hours:
            canonical_date = date.fromisoformat(json_date_events["date"])

            for json_event in json_date_events["events"]:
                events.append(DiningHallEvent(
                    description=json_event["descr"],
                    canonical_date=canonical_date,
                    start_timestamp=json_event["startTimestamp"],
                    end_timestamp=json_event["endTimestamp"],
                    menu=CornellDiningNow.dining_hall_menu_from_json(json_event["menu"])
                ))

        return events

    @staticmethod
    def dining_hall_menu_from_json(json_menu: list) -> DiningHallMenu:
        json_menu = sorted(
            json_menu,
            key=lambda json_menu_category: json_menu_category["sortIdx"]
        )
        menu_categories = []

        for json_menu_category in json_menu:
            items = [
                MenuItem.from_cornell_dining_json(json_item)
                for json_item in json_menu_category["items"]
            ]

            menu_categories.append(DiningHallMenuCategory(
                category=json_menu_category["category"],
                items=items
            ))

        return DiningHallMenu(categories=menu_categories)

    def description(self):
        return "CornellDiningNow"
