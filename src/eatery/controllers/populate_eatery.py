import requests 

from eatery.datatype.Eatery import Eatery, EateryID
from eatery.serializers import EaterySerializer
from eatery.models import Eatery


class PopulateEateryController:
    def __init__(self):
        self = self
    
    def generate_eatery(self, json_eatery):
        """
        Create Eatery object from json and add to Eatery table
        """

        data = {
            "id" : json_eatery["id"],
            "name":json_eatery["name"],
            "campus_area":json_eatery["campusArea"]["descrshort"],
            "latitude":json_eatery["latitude"],
            "longitude":json_eatery["longitude"],
            "payment_accepts_cash":True,
            "payment_accepts_brbs":any(
                [
                    method["descrshort"] == "Meal Plan - Debit"
                    for method in json_eatery["payMethods"]
                ]
            ),
            "payment_accepts_meal_swipes":any(
                [
                    method["descrshort"] == "Meal Plan - Swipe"
                    for method in json_eatery["payMethods"]
                ]
            ),
            "location":json_eatery["location"],
            "online_order_url":json_eatery["onlineOrderUrl"]
        }

        eatery = EaterySerializer(data=data)
        if eatery.is_valid():
            eatery.save()
        else:
            print(eatery.errors)
            
    def process(self, json_eateries):
        
        for json_eatery in json_eateries: 
            self.generate_eatery(json_eatery)
