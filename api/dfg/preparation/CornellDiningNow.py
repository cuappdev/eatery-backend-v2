import requests

from api.dfg.DfgNode import DfgNode
from api.dfg.preparation.datatype.CornellDiningEatery import CornellDiningEatery
from api.dfg.preparation.datatype.Event import Event
from api.dfg.preparation.datatype.Menu import Menu
from api.dfg.preparation.datatype.MenuCategory import MenuCategory
from api.dfg.preparation.datatype.MenuItem import MenuItem

from datetime import date


class CornellDiningNow(DfgNode):

    CORNELL_DINING_URL = "https://now.dining.cornell.edu/api/1.0/dining/eateries.json"

    def __call__(self, *args, **kwargs) -> list[CornellDiningEatery]:
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
    def parse_eatery(json_eatery: dict) -> CornellDiningEatery:
        is_cafe = "Cafe" in {
            eatery_type["descr"]
            for eatery_type in json_eatery["eateryTypes"]
        }
        return CornellDiningEatery(
            name=json_eatery["name"],
            about=json_eatery["about"],
            about_short=json_eatery["aboutshort"],
            campus_area=json_eatery["campusArea"]["descrshort"],
            latitude=json_eatery["latitude"],
            longitude=json_eatery["longitude"],
            events=CornellDiningNow.eatery_events_from_json(
                json_operating_hours=json_eatery["operatingHours"],
                json_dining_items = json_eatery["diningItems"],
                is_cafe = is_cafe
            ),
            payment_methods=CornellDiningNow.generate_payment_methods(json_eatery["payMethods"]),
            location=json_eatery["location"],
            online_order=json_eatery["onlineOrdering"],
            online_order_url=json_eatery["onlineOrderUrl"]
        )

    @staticmethod
    def generate_payment_methods(json_paymethods: list):
        payment_methods = []
        takes_cash = True
        takes_brbs = any([method["descrshort"] == "Meal Plan - Debit" for method in json_paymethods])
        takes_swipes = any([method["descrshort"] == "Meal Plan - Swipe" for method in json_paymethods])
        if takes_cash:
            payment_methods.append("cash")
        if takes_brbs:
            payment_methods.append("brbs")
        if takes_swipes:
            payment_methods.append("swipes")
        return payment_methods

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
