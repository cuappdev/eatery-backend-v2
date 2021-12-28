from typing import Union

from api.dfg.DfgNode import DfgNode
import requests
from api.datatype.Eatery import Eatery
from api.datatype.Event import Event
from api.datatype.Menu import Menu
from api.datatype.MenuCategory import MenuCategory
from api.datatype.MenuItem import MenuItem
from datetime import date


class CornellDiningNow(DfgNode):

    CORNELL_DINING_URL = "https://now.dining.cornell.edu/api/1.0/dining/eateries.json"

    def __call__(self, *args, **kwargs) -> list[Eatery]:
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
    def parse_eatery(json_eatery: dict) -> Eatery:
        is_cafe = "Cafe" in {
            eatery_type["descr"]
            for eatery_type in json_eatery["eateryTypes"]
        }
        return Eatery(
            name=json_eatery["name"],
            campus_area=json_eatery["campusArea"]["descrshort"],
            latitude=json_eatery["latitude"],
            longitude=json_eatery["longitude"],
            events=CornellDiningNow.eatery_events_from_json(
                json_operating_hours=json_eatery["operatingHours"],
                json_dining_items = json_eatery["diningItems"],
                is_cafe = is_cafe
            ),

        )

    @staticmethod
    def eatery_events_from_json(json_operating_hours: list, json_dining_items: list, is_cafe: bool) -> list[Event]:
        json_operating_hours = sorted(
            json_operating_hours,
            key=lambda json_date_events: json_date_events["date"]
        )
        events = []

        for json_date_events in json_operating_hours:
            canonical_date = date.fromisoformat(json_date_events["date"])

            for json_event in json_date_events["events"]:
                events.append(Event(
                    canonical_date=canonical_date,
                    description=json_event["descr"],
                    start_timestamp=json_event["startTimestamp"],
                    end_timestamp=json_event["endTimestamp"],
                    menu=CornellDiningNow.eatery_menu_from_json(json_event["menu"], json_dining_items, is_cafe)
                ))

        return events

    @staticmethod
    def eatery_menu_from_json(json_menu: list, json_dining_items: list, is_cafe: bool):
        if is_cafe:
            return CornellDiningNow.cafe_menu_from_json(json_dining_items)
        else:
            return CornellDiningNow.dining_hall_menu_from_json(json_menu)

    @staticmethod
    def cafe_menu_from_json(json_dining_items: list) -> Menu:
        category_map = {}
        for item in json_dining_items:
            if item['category'] not in category_map:
                category_map[item['category']] = []
            category_map[item['category']].append(MenuItem(healthy=item['healthy'], name = item['item']))
        categories = []
        for category_name in category_map:
            categories.append(MenuCategory(category_name, category_map[category_name]))
        return Menu(categories=categories)
    
    @staticmethod
    def dining_hall_menu_from_json(json_menu: list) -> Menu:
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

            menu_categories.append(MenuCategory(
                category=json_menu_category["category"],
                items=items
            ))

        return Menu(categories=menu_categories)

    def description(self):
        return "CornellDiningNow"
