from item.models import Item
from item.serializers import ItemSerializer
from eatery.models import Eatery
from eatery.serializers import EaterySerializer

class PopulateItemController():
    def __init__(self):
        self = self 

    def generate_cafe_items(self, json_eatery):
        for json_item in json_eatery["diningItems"]: 
            data = {
                "eatery" : int(json_eatery["id"]),
                "name" : json_item["item"]
            }
            item = ItemSerializer(data=data)
            if item.is_valid():
                item.save()
            else:
                print('error')
                return item.errors 
        

    def generate_dining_hall_items(self, json_event, json_eatery):
        json_menus = json_event['menu']
        for json_menu in json_menus:
            for json_item in json_menu['items']: 
                data = {
                    "eatery" : int(json_eatery["id"]),
                    "name" : json_item["item"]
                }
                item = ItemSerializer(data=data)
                if item.is_valid():
                    item.save()
                else: 
                    return item.errors 

    def process(self, menus_dict, json_eateries):
        for json_eatery in json_eateries:

            is_cafe = "Cafe" in {
                eatery_type["descr"] for eatery_type in json_eatery["eateryTypes"]
            }  
            json_dates = json_eatery["operatingHours"]
            for json_date in json_dates: 
                json_events = json_date["events"]
                for json_event in json_events:

                    if is_cafe: 
                        self.generate_cafe_items(json_eatery)
                    else: 
                        self.generate_dining_hall_items(json_event, json_eatery)
