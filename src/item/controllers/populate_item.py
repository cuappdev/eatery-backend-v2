from item.models import Item
from item.serializers import ItemSerializer

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
                return item.errors 
        

    def generate_dining_hall_items(self, json_event, eatery_id):
        for json_menu in json_event:
            for json_menu_category in json_menu: 
                for json_item in json_menu_category["items"]: 
                    data = {
                        "eatery" : eatery_id,
                        "name" : json_item["item"]
                    }
                    item = ItemSerializer(data=data)
                    if item.is_valid():
                        item.save()
                    else: 
                        return item.errors 

    def process(self, json_eateries):
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
                        self.generate_dining_hall_items(json_event, int(json_eatery["id"]))
