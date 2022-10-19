from eatery.models import EateryStore
from eatery.util.constants import CORNELL_DINING_URL, dining_id_to_internal_id

import requests


class PopulateMenuController:

    def __init__(self):
        self = self
    
    """ TODO: THIS SHOULD BE IN A CENTRALIZED AREA! 
    it's here just for quick implementation purposes """
    def get_json(self):
        """
        Get json from CornellDiningNow, separate by eatery
        """
        try:
            response = requests.get(CORNELL_DINING_URL).json()
        except Exception as e:
            raise e
        if response["status"] == "success":
            json_eateries = response["data"]["eateries"]
        return json_eateries