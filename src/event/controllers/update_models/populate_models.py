"""
Populate the eatery models with CornellDiningNow() data.

Basically functions the same way as a DFG main.py.
This is.... worse than the initial implementation (solely bc I am not technically skilled pfft)

Implementing ViewSets will reduce the amount of code in here. 
"""
from datetime import date, datetime

import requests

from event.models import Event, Menu, Category, Item, SubItem, CategoryItemAssociation
from event.serializers import EventSerializer, MenuSerializer, CategorySerializer

from eatery.util.constants import CORNELL_DINING_URL, dining_id_to_internal_id


class CornellDiningNowController():
    def __init__(self, cache):
        self.cache = cache
        
    def __call__(self):
        return


    """
    return json of eateries from CDN
    """
    def get_json(self):
        try:
            response = requests.get(CORNELL_DINING_URL).json()
        except Exception as e:
            raise e
        if response["status_code"] <= 400:
            json_eateries = response["data"]["eateries"]
        return json_eateries


    # Populate events 
    def generate_events(self, json_eatery):
        is_cafe = "Cafe" in {
            eatery_type["descr"] for eatery_type in json_eatery["eateryTypes"]
        }  
        json_dates = json_eatery["operatingHours"]

        for json_date in json_dates:
            canon_date = date.fromisoformat(json_date["date"])

            json_events = json_date["events"]
            
            for json_event in json_events:
                start_time = datetime.fromtimestamp(json_event["startTimestamp"])
                end_time = datetime.fromtimestamp(json_event["endTimestamp"])

                start = datetime.combine(canon_date, start_time)
                end = datetime.combine(canon_date, end_time)

                # create event 
                event = Event.objects.create(
                    eatery = json_eatery["id"],
                    event_description = json_event["descr"],
                    start = start,
                    end = end
                )
                event.save()
                event = EventSerializer(event)

                if is_cafe: 
                    self.generate_cafe_menus(json_eatery, json_event, event)
                else: 
                    self.generate_dining_hall_menus(json_eatery, json_event, event)

                
    # these create functions should be in the serializers. ViewSets will probably take these out
    def create_menu(event_id): 
        menu = Menu.objects.create(
            event = event_id
        )
        menu.save()
        return menu
                
    def create_menu_item(json_eatery, json_item):
        item = Item.objects.create(
            eatery = json_eatery["id"], 
            name = json_item["item"]   
        )
        item.save()
        return item

    def create_category(json_menu_category, menu_id):
        category = Category.objects.create(
            menu = menu_id, 
            category = json_menu_category["category"]
        )
        category.save()
        return category


    # Populate menus
    def generate_dining_hall_menus(self, json_eatery, json_event, event_serialized):
        event_id = event_serialized['id']

        for json_menu in json_event:
            json_menu = sorted(json_menu, key=lambda json_menu_category: json_menu_category["sortIdx"])
            
            menu = self.create_menu(event_id)
            menu = MenuSerializer(menu)

            for json_menu_category in json_menu:
                category = self.create_category(json_menu_category, menu['id'])
                category = CategorySerializer(category)
                
                for json_item in json_menu_category["items"]:
                    item = self.create_menu_item(json_eatery, json_item)
    
    def generate_cafe_menus(self, json_eatery, json_event, event_serialized):
        event = event_serialized
        menu = self.create_menu(event['id']) 
        menu = MenuSerializer(menu)

        category_map = {}
        dining_items = json_eatery["diningItems"]

        for item in dining_items: 
            if item["category"] not in category_map:
                category_map[item["category"]] = []

            category_map[item["category"]].append(
                item = self.create_menu_item(json_eatery, item))

        for category_name in category_map:
            self.create_category(menu['id'], category_map[category_name])


    def process(self):
        json_eateries = self.get_json()

        for json_eatery in json_eateries:
            self.generate_events(json_eatery)

        
    

        