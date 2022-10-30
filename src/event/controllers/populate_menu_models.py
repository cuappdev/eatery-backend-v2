import json
from eatery.models import Eatery
from event.models import EventModel, EventScheduleModel, MenuModel
from eatery.util.constants import CORNELL_DINING_URL, dining_id_to_internal_id

import requests


class PopulateMenuController:

    def __init__(self, json_eateries: json):
        self.json_eateries = json_eateries


        #models.Shop.objects.order_by().values_list('city').distinct()

        
    def generate_events(self):

        for operating_hours in self.json_eateries["operatingHours"]


    # event -> menu -> category -> items -> subitems 

    def generate_menus(self):
        json_eateries = self.get_json()

        for json_eatery in json_eateries:
            "Cafe" in json_eatery["description"]


    def generate_cafe_menu(self):
        category_map = {}

        EventStore.objects.create(
            eatery = 
            
        )



    def generate_dining_hall_menu(self):
        pass



    def generate_category(self):
        pass

    def generate_item(self):
        pass

    # Subitems  are specifications of items. small/medium/etc... 
    def generate_subitem(self):
        pass



