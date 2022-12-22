from datetime import date

import requests
from event.datatype.Event import Event
from api.datatype.Menu import Menu
from api.datatype.MenuCategory import MenuCategory
from api.datatype.MenuItem import MenuItem
from api.dfg.nodes.DfgNode import DfgNode
from api.util.constants import CORNELL_DINING_URL, dining_id_to_internal_id
from eatery.datatype.Eatery import Eatery, EateryID


class CornellDiningEvents(DfgNode):
    def __init__(self, eatery_id: EateryID, cache):
        self.eatery_id = eatery_id
        self.cache = cache

    def __call__(self, *args, **kwargs) -> list[Eatery]:
        if "eateries" not in self.cache:
            try:
                response = requests.get(CORNELL_DINING_URL).json()
            except Exception as e:
                raise e
            if response["status"] == "success":
                json_eateries = response["data"]["eateries"]
                eateries = []
                for json_eatery in json_eateries:
                    eateries.append(CornellDiningEvents.parse_eatery(json_eatery))
                self.cache["eateries"] = eateries
        for eatery in self.cache["eateries"]:
            if eatery.id == self.eatery_id:
                return eatery.events()
        return []

    @staticmethod
    def parse_eatery(json_eatery: dict) -> Eatery:
        is_cafe = "Cafe" in {
            eatery_type["descr"] for eatery_type in json_eatery["eateryTypes"]
        }
        return Eatery(
            id=dining_id_to_internal_id(json_eatery["id"]),
            events=CornellDiningEvents.eatery_events_from_json(
                json_operating_hours=json_eatery["operatingHours"],
                json_dining_items=json_eatery["diningItems"],
                is_cafe=is_cafe,
            ),
        )

    @staticmethod
    def eatery_events_from_json(
        json_operating_hours: list, json_dining_items: list, is_cafe: bool
    ) -> list[Event]:
        json_operating_hours = sorted(
            json_operating_hours, key=lambda json_date_events: json_date_events["date"]
        )
        events = []

        for json_date_events in json_operating_hours:
            canonical_date = date.fromisoformat(json_date_events["date"])

            for json_event in json_date_events["events"]:
                events.append(
                    Event(
                        canonical_date=canonical_date,
                        description=json_event["descr"],
                        start_timestamp=json_event["startTimestamp"],
                        end_timestamp=json_event["endTimestamp"],
                        menu=CornellDiningEvents.eatery_menu_from_json(
                            json_event["menu"], json_dining_items, is_cafe
                        ),
                    )
                )

        return events

    @staticmethod
    def eatery_menu_from_json(json_menu: list, json_dining_items: list, is_cafe: bool):
        if is_cafe:
            return CornellDiningEvents.cafe_menu_from_json(json_dining_items)
        else:
            return CornellDiningEvents.dining_hall_menu_from_json(json_menu)

    @staticmethod
    def cafe_menu_from_json(json_dining_items: list) -> Menu:
        category_map = {}
        for item in json_dining_items:
            if item["category"] not in category_map:
                category_map[item["category"]] = []
            category_map[item["category"]].append(
                MenuItem(healthy=item["healthy"], name=item["item"])
            )
        categories = []
        for category_name in category_map:
            categories.append(MenuCategory(category_name, category_map[category_name]))
        return Menu(categories=categories)

    @staticmethod
    def dining_hall_menu_from_json(json_menu: list) -> Menu:
        json_menu = sorted(
            json_menu, key=lambda json_menu_category: json_menu_category["sortIdx"]
        )
        menu_categories = []

        for json_menu_category in json_menu:
            items = [
                CornellDiningEvents.from_cornell_dining_json(json_item)
                for json_item in json_menu_category["items"]
            ]

            menu_categories.append(
                MenuCategory(category=json_menu_category["category"], items=items)
            )

        return Menu(categories=menu_categories)

    @staticmethod
    def from_cornell_dining_json(json_item: dict):
        return MenuItem(
            healthy=json_item["healthy"],
            name=json_item["item"]
        )

    def description(self):
        return "CornellDiningEvents"
