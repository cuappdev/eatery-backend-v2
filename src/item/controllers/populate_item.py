from item.models import Item
from item.serializers import ItemSerializer
from eatery.models import Eatery
from eatery.serializers import EaterySerializer
import string
import json

class PopulateItemController():
    def __init__(self):
        self = self 

    def generate_cafe_items(self, menu, json_eatery):

        for json_item in json_eatery["diningItems"]: 

            category_name = json_item['category'].strip()
            category_id = menu[category_name]

            data = {
                "category" : category_id,
                "name" : json_item["item"]
            }
            item = ItemSerializer(data=data)
            if item.is_valid():
                item.save()
            else:
                print(item.errors)
        

    def generate_dining_hall_items(self, menu, json_event, json_eatery):
        json_menus = json_event['menu']
        for json_menu in json_menus:

            category_name = json_menu['category'].strip()
            category_id = menu[category_name]

            for json_item in json_menu['items']: 
                data = {
                    "category" : category_id,
                    "name" : json_item["item"]
                }
                item = ItemSerializer(data=data)
                if item.is_valid():
                    item.save()
                else: 
                    print(item.errors) 

    def process(self, categories_dict, json_eateries):
        with open("./static_sources/external_eateries.json", "r") as file:
            json_obj = json.load(file)
            json_eateries += json_obj["eateries"]

        for json_eatery in json_eateries:
            if int(json_eatery["id"]) in categories_dict:
                eatery_menus = categories_dict[int(json_eatery["id"])]
            else:
                continue

            iter = list(eatery_menus.keys())
            i = 0

            is_cafe = not "Dining Room" in {eatery_type["descr"] for eatery_type in json_eatery["eateryTypes"]}

            json_dates = json_eatery["operatingHours"]
            for json_date in json_dates: 
                json_events = json_date["events"]
                for json_event in json_events:
                    if i < len(iter):
                        menu_id = iter[i]
                        menu = eatery_menus[menu_id]; i += 1

                    if is_cafe: 
                        self.generate_cafe_items(menu, json_eatery)
                    else: 
                        self.generate_dining_hall_items(menu, json_event, json_eatery)
