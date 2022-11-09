"""
Populate the eatery models with CornellDiningNow() data.

Basically functions the same way as a DFG main.py.
This is.... worse than the initial implementation (solely bc I am not technically skilled pfft)

Implementing ViewSets will reduce the amount of code in here. 
"""

from datetime import datetime

import requests

from event.serializers import *
from event.models import *

from eatery.util.constants import CORNELL_DINING_URL, dining_id_to_internal_id

class PopulateEventController():
    def __init__(self):
        self = self


    def generate_events(self, json_eatery):
        is_cafe = "Cafe" in {
            eatery_type["descr"] for eatery_type in json_eatery["eateryTypes"]
        }  
        json_dates = json_eatery["operatingHours"]

        for json_date in json_dates:
            canon_date = datetime.fromisoformat(json_date["date"])
            json_events = json_date["events"]
            
            for json_event in json_events:
                event = self.create_event(json_eatery, json_event, canon_date)

            

                if is_cafe: 
                    self.generate_cafe_menus(json_eatery, json_event, event)
                else: 
                    self.generate_dining_hall_menus(json_eatery, json_event, event)


    def create_event_datetime(self, json_event, date):
        """
        merge date and timestamp for creating event.
        return {'start': start, 'end': end}
        """
        start_time = datetime.fromtimestamp(json_event["startTimestamp"])
        end_time = datetime.fromtimestamp(json_event["endTimestamp"])
        start = datetime.combine(date, start_time.time())
        end = datetime.combine(date, end_time.time())

        return {"start" : start, "end": end}

    def create_event(self, json_eatery, json_event, canon_date):
        dates = self.create_event_datetime(json_event, canon_date)
        start = dates['start']
        end = dates['end']

        data = {'eatery': int(json_eatery["id"]),
                'event_description': json_event["descr"],
                'start' : start,
                'end' : end }

        event = EventSerializer(data=data)
        if event.is_valid():
            event.save()
        else:
            return event.errors 
        return event


    def generate_dining_hall_menus(self, json_eatery, json_event, event):
        """
        Create menu >> category >> item objects. 
        (this is messy but it's how i intuitively understand it)
        """

        for json_menu in json_event:
            #json_menu = sorted(json_menu, key=lambda json_menu_category: json_menu_category["sortIdx"])
            if event.is_valid():
                menu = MenuSerializer(data={"event": int(event.data['id'])})

            if not menu.is_valid():
                return menu.errors

            for json_menu_category in json_menu:
                if menu.is_valid():
                    category = CategorySerializer(data={"menu": int(menu.data['id']), "category": json_menu_category["category"]})
                if not category.is_valid():
                    return category.errors 

                for json_item in json_menu_category["items"]:
                    item = ItemSerializer(data={"eatery": int(json_eatery["id"]), "name" : json_item["item"] })
                    if not item.is_valid():
                        return item.errors
    

    def generate_cafe_menus(self, json_eatery, json_event, event):
        if event.is_valid():
            event_id = int(event.data['id'])
            menu = MenuSerializer(data={"event":event_id})

        category_map = {}
        dining_items = json_eatery["diningItems"]

        for item in dining_items: 
            if item["category"] not in category_map:
                category_map[item["category"]] = []

            ser_item = ItemSerializer(data={"eatery": int(json_eatery["id"]), "name" : item })
            if ser_item.is_valid(): 
                ser_item.save()

            category_map[item["category"]] = item
            
        for category_name in category_map:
            if menu.is_valid():
                category = CategorySerializer(data={"menu": int(menu.data['id']), "category": category_map[category_name]})
            
                if category.is_valid():
                    category.save()

    def process(self, json_eateries):
        
        for json_eatery in json_eateries:
            self.generate_events(json_eatery)

    