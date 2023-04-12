import requests
import json
from eatery.datatype.Eatery import EateryID
from eatery.util.constants import dining_id_to_internal_id, SnapshotFileName
from eatery.serializers import EaterySerializer
from eatery.models import Eatery


class PopulateEateryController:
    def __init__(self):
        self = self

    def generate_eatery(self, json_eatery):
        """
        Create Eatery object from an eatery json from CornellDiningNow, and add to Eatery table.
        """
        eatery_id = dining_id_to_internal_id(json_eatery["id"]).value

        data = {
            "id": eatery_id,
            "name": json_eatery["name"],
            "campus_area": json_eatery["campusArea"]["descrshort"],
            "latitude": json_eatery["latitude"],
            "longitude": json_eatery["longitude"],
            "payment_accepts_cash": True,
            "payment_accepts_brbs": any(
                [
                    method["descrshort"] == "Meal Plan - Debit"
                    for method in json_eatery["payMethods"]
                ]
            ),
            "payment_accepts_meal_swipes": any(
                [
                    method["descrshort"] == "Meal Plan - Swipe"
                    for method in json_eatery["payMethods"]
                ]
            ),
            "location": json_eatery["location"],
            "online_order_url": json_eatery["onlineOrderUrl"],
        }

        eatery = EaterySerializer(data=data)
        if eatery.is_valid():
            eatery.save()
        else:
            print(eatery.errors)

    def add_eatery_store(self):
        """
        Create eatery objects from an eatery json from a eatery_db_snapshot, and add to Eatery table.
        """

        folder_path = "./eatery/util/"
        file_name = SnapshotFileName.EATERY_STORE

        with open(f"{folder_path}{file_name.value}", "r") as file:
            json_objs = []
            for line in file:
                if len(line) > 2:
                    json_objs.append(json.loads(line))
            
            for json_obj in json_objs:
                try:
                    object = Eatery.objects.get(id=int(json_obj["id"]))
                except object.DoesNotExist:
                    """
                    Create a new Eatery object
                    """
                    serialized = EaterySerializer(data=json_obj)
                else:
                    """
                    Update already-existing Eatery object
                    """
                    serialized = EaterySerializer(object, data=json_obj, partial=True)

                if serialized.is_valid():
                    serialized.save()
                else:
                    print(serialized.errors)

    def process(self, json_eateries):
        for json_eatery in json_eateries:
            self.generate_eatery(json_eatery)

        self.add_eatery_store()
