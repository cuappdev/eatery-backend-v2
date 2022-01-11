import requests

from api.dfg.DfgNode import DfgNode

from api.datatype.Eatery import Eatery
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
            payment_methods=CornellDiningNow.generate_payment_methods(json_eatery["payMethods"]),
            location=json_eatery["location"],
            online_order_url=json_eatery["onlineOrderUrl"]
        )

    @staticmethod
    def generate_payment_methods(json_paymethods: list):
        payment_methods = []
        takes_cash = True
        takes_brbs = any([method["descrshort"] == "Meal Plan - Debit" for method in json_paymethods])
        takes_swipes = any([method["descrshort"] == "Meal Plan - Swipe" for method in json_paymethods])
        if takes_cash:
            payment_methods.append("cash")
        if takes_brbs:
            payment_methods.append("brbs")
        if takes_swipes:
            payment_methods.append("swipes")
        return payment_methods

    def description(self):
        return "CornellDiningNow"
