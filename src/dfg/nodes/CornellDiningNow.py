import requests

from dfg.nodes.DfgNode import DfgNode

from dfg.datatype.Eatery import Eatery
from util.constants import dining_id_to_internal_id, CORNELL_DINING_URL

from datetime import date

class CornellDiningNow(DfgNode):

    def __call__(self, *args, **kwargs) -> list[Eatery]:
        try:
            response = requests.get(CORNELL_DINING_URL).json()

        except Exception as e:
            raise e

        if response["status"] == "success":
            json_eateries = response["data"]["eateries"]
            eateries = []
            for json_eatery in json_eateries:
                eateries.append(CornellDiningNow.parse_eatery(json_eatery))
            return eateries

        else:
            raise Exception(response["message"])

    @staticmethod
    def parse_eatery(json_eatery: dict) -> Eatery:
        # Events are parsed later
        return Eatery(
            id=dining_id_to_internal_id(json_eatery["id"]),
            name=json_eatery["name"],
            campus_area=json_eatery["campusArea"]["descrshort"],
            latitude=json_eatery["latitude"],
            longitude=json_eatery["longitude"],
            payment_accepts_cash=True,
            payment_accepts_brbs=any([method["descrshort"] == "Meal Plan - Debit" for method in json_eatery["payMethods"]]),
            payment_accepts_meal_swipes=any([method["descrshort"] == "Meal Plan - Swipe" for method in json_eatery["payMethods"]]),
            location=json_eatery["location"],
            online_order_url=json_eatery["onlineOrderUrl"]
        )

    def description(self):
        return "CornellDiningNow"
