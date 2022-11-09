import requests 

from eatery.datatype.Eatery import Eatery, EateryID
from eatery.serializers import EaterySerializer
from eatery.models import Eatery
from eatery.util.constants import CORNELL_DINING_URL, dining_id_to_internal_id


class PopulateEateryController:
    def __init__(self):
        self = self
    
    def get_json(self):
        """
        Get json from CornellDiningNow, separate by eatery
        """
        try:
            response = requests.get(CORNELL_DINING_URL)
        except Exception as e:
            raise e
        if response.status_code <= 400 :
            response = response.json()
            json_eateries = response["data"]["eateries"]

        return json_eateries


    def generate_eatery(self, json_eatery) -> Eatery:
        """
        Create Eatery object from json and add to Eatery table
        """
        eatery = EaterySerializer(
            id=json_eatery["id"],#dining_id_to_internal_id(json_eatery["id"]),
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
        if eatery.is_valid():
            eatery.save()
        else:
            eatery.errors 
            
        return eatery

    def process(self):
        json_eateries = self.get_json()

        for json_eatery in json_eateries: 
            self.generate_eatery(json_eatery)
