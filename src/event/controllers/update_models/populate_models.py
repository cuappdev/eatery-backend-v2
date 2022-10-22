"""
Populate the eatery models with CornellDiningNow() data.

Basically functions the same way as a DFG main.py...
"""
from datetime import date 

import json
from eatery.datatype.Eatery import Eatery, EateryID

from event.datatype.Event import Event
from api.datatype.Menu import Menu
from api.datatype.MenuCategory import MenuCategory
from api.datatype.MenuItem import MenuItem

from api.util.constants import CORNELL_DINING_URL, dining_id_to_internal_id
import requests


class CornellDiningNowController():
    def __init__(self, cache):
        self.cache = cache
        
    def __call__(self):
        return

    @staticmethod
    def process(self):
        """
        Populate 
        """
        try:
            response = requests.get(CORNELL_DINING_URL).json()
        except Exception as e:
            raise e
        if response["status"] == "success":
            json_eateries = response["data"]["eateries"]
        return json_eateries


    def revert_all_models():
        json_eateries = CornellDiningNow.get_json()

        for json_eatery in json_eateries:
            generate_eatery(json_eatery)

            generate_event(json_eatery)



            populate_event(json_eatery)

    def generate_event(json_eatery) -> Event: 

        json_operating_hours=json_eatery["operatingHours"]
        json_dining_items=json_eatery["diningItems"]
        
        for json_date_events in json_operating_hours:
            canonical_date = date.fromisoformat(json_date_events["date"])


    """
    Add Eatery object to model.
    """cc
    @staticmethod
    def generate_eatery(json_eatery) -> Eatery:
        eatery = Eatery(
            id=dining_id_to_internal_id(json_eatery["id"]),
            name=json_eatery["name"],
            campus_area=json_eatery["campusArea"]["descrshort"],
            latitude=json_eatery["latitude"],
            longitude=json_eatery["longitude"],
            payment_accepts_cash=True,
            payment_accepts_brbs=any(
                [
                    method["descrshort"] == "Meal Plan - Debit"
                    for method in json_eatery["payMethods"]
                ]
            ),
            payment_accepts_meal_swipes=any(
                [
                    method["descrshort"] == "Meal Plan - Swipe"
                    for method in json_eatery["payMethods"]
                ]
            ),
            location=json_eatery["location"],
            online_order_url=json_eatery["onlineOrderUrl"],
        )
        eatery.save()

        return eatery

    """
    Add Event object to model
    ((placeholder -- ))
    """


    """
    Every menu is an Event type.
    """

    def populate_event(json, eatery):
        json_eatery = json
        pass

        

    def populate_cafe_menuitem():
        pass

    def populate_dininghall_menuitem():
        pass

    
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


    def dining_hall_menu_from_json(json_menu: list) -> Menu:
        json_menu = sorted(
            json_menu, key=lambda json_menu_category: json_menu_category["sortIdx"]
        )
        menu_categories = []

        for json_menu_category in json_menu:
            items = [
                from_cornell_dining_json(json_item)
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


    # I don't see alerts anywhere in the json? is this a newly added thing for EateryChef?
    def populate_alert_model(json, eatery):
        pass 

    def populate_report_model():
        pass

    """
    Populates all models with menu information from CornellDiningNow()
    (TODO: check with currently cached data)
    """
    





        
    

        