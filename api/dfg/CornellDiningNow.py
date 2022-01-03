import requests

from api.dfg.DfgNode import DfgNode

from api.datatype.Eatery import Eatery, EateryID
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
            id=CornellDiningNow.dining_id_to_internal_id(json_eatery["id"]),
            name=json_eatery["name"],
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
                    menu=CornellDiningNow.eatery_menu_from_json(json_event["menu"], json_dining_items, is_cafe),
                    exists=True
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

    @staticmethod
    def dining_id_to_internal_id(id: int):
        if id == 31:
            return EateryID.ONE_ZERO_FOUR_WEST
        elif id == 7:
            return EateryID.LIBE_CAFE
        elif id == 8:
            return EateryID.ATRIUM_CAFE
        elif id == 1:
            return EateryID.BEAR_NECESSITIES
        elif id == 25:
            return EateryID.BECKER_HOUSE
        elif id == 10:
            return EateryID.BIG_RED_BARN
        elif id == 11:
            return EateryID.BUS_STOP_BAGELS
        elif id == 12:
            return EateryID.CAFE_JENNIE
        elif id == 2:
            return EateryID.CAROLS_CAFE
        elif id == 26:
            return EateryID.COOK_HOUSE
        elif id == 14:
            return EateryID.DAIRY_BAR
        elif id == 41:
            return EateryID.CROSSINGS_CAFE
        elif id == 32:
            return EateryID.FRANNYS
        elif id == 16:
            return EateryID.GOLDIES_CAFE
        elif id == 15:
            return EateryID.GREEN_DRAGON
        elif id == 24:
            return EateryID.HOT_DOG_CART
        elif id == 34:
            return EateryID.ICE_CREAM_BIKE
        elif id == 27:
            return EateryID.BETHE_HOUSE
        elif id == 28:
            return EateryID.JANSENS_MARKET
        elif id == 29:
            return EateryID.KEETON_HOUSE
        elif id == 42:
            return EateryID.MANN_CAFE 
        elif id == 18:
            return EateryID.MARTHAS_CAFE
        elif id == 19:
            return EateryID.MATTINS_CAFE
        elif id == 33:
            return EateryID.MCCORMICKS 
        elif id == 3:
            return EateryID.NORTH_STAR_DINING
        elif id == 20:
            return EateryID.OKENSHIELDS
        elif id == 4:
            return EateryID.RISLEY
        elif id == 5:
            return EateryID.RPCC 
        elif id == 30:
            return EateryID.ROSE_HOUSE
        elif id == 21:
            return EateryID.ROSE_HOUSE
        elif id == 13:
            return EateryID.STRAIGHT_FROM_THE_MARKET
        elif id == 23:
            return EateryID.TERRACE
        else:
            return EateryID.NULL

    def description(self):
        return "CornellDiningNow"
