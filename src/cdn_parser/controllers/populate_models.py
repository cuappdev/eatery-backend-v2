import requests 
from eatery.util.constants import CORNELL_DINING_URL, dining_id_to_internal_id

from eatery.controllers.populate_eatery import PopulateEateryController
from event.controllers.populate_event import PopulateEventController
from menu.controllers.populate_menu import PopulateMenuController
from item.controllers.populate_item import PopulateItemController
from category.controllers.populate_category import PopulateCategoryController

class CornellDiningNowController():
    def __init__(self):
        self = self 

    def get_json(self):
        try:
            response = requests.get(CORNELL_DINING_URL)
        except Exception as e:
            raise e
        if response.status_code <= 400:
            response = response.json()
            json_eateries = response["data"]["eateries"]
        return json_eateries

    def process(self):
        """
        Get JSON from API 
        create eateries 

        >> json_date in json_dates
        >> json_event in json_events 

        create events

        >> json_menu in json_event

        create menus 

        >> json_menu_category in json_menu
        +>> json_item in json_menu_category

        create items 

        create categories 
        """

        json_eateries = self.get_json()

        PopulateEateryController().process(json_eateries)

        events_dict = PopulateEventController().process(json_eateries)    

        menus_dict = PopulateMenuController().process(events_dict, json_eateries)

        categories_dict = PopulateCategoryController().process(menus_dict, json_eateries)

        PopulateItemController().process(categories_dict, json_eateries)


        


    
