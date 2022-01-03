from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime, timedelta, tzinfo
from random import randrange
import pytz

from transactions.models import TransactionHistory
class UpdateTransactionsController:

    # Converts the Vendor's name for the eatery into the name stored in our backend
    @staticmethod
    def vendor_name_to_internal_id(vendor_eatery_name):
        vendor_eatery_name = ''.join(c.lower() for c in vendor_eatery_name if c.isalpha())
        if vendor_eatery_name == "bearnecessities":
            return 4
        elif vendor_eatery_name == "northstarmarketplace":
            return 25
        elif vendor_eatery_name == "jansensmarket":
            return 19
        elif vendor_eatery_name == "stockinghallcafe" or vendor_eatery_name == "stockinghall":
            return 11
        elif vendor_eatery_name == "marthas":
            return 22
        elif vendor_eatery_name == "cafejennie":
            return 8
        elif vendor_eatery_name == "goldiescafe":
            return 14
        elif vendor_eatery_name == "alicecookhouse":
            return 10
        elif vendor_eatery_name == "carlbeckerhouse":
            return 5
        elif vendor_eatery_name == "duffield":
            return 23
        elif vendor_eatery_name == "greendragon":
            return 15
        elif vendor_eatery_name == "trillium":
            return 32
        elif vendor_eatery_name == "olinlibecafe":
            return 2
        elif vendor_eatery_name == "carolscafe":
            return 9
        elif vendor_eatery_name == "statlerterrace":
            return 33
        elif vendor_eatery_name == "busstopbagels":
            return 7
        elif vendor_eatery_name == "kosher":
            return 1
        elif vendor_eatery_name == "jansensatbethehouse":
            return 18
        elif vendor_eatery_name == "keetonhouse":
            return 20
        elif vendor_eatery_name == "rpme":
            return 28
        elif vendor_eatery_name == "rosehouse":
            return 29
        elif vendor_eatery_name == "risley":
            return 27
        elif vendor_eatery_name == "frannysft":
            return 13
        elif vendor_eatery_name == "mccormicks":
            return 24
        elif vendor_eatery_name == "sage":
            return 3
        elif vendor_eatery_name == "straightmarket":
            return 31
        elif vendor_eatery_name == "crossingscafe":
            return 12
        elif vendor_eatery_name == "okenshields":
            return 26
        elif vendor_eatery_name == "bigredbarn":
            return 6
        elif vendor_eatery_name == "rustys":
            return 30
        elif vendor_eatery_name == "manncafe":
            return 21
        elif vendor_eatery_name == "statlermacs":
            return 34
        else:
            # TODO: Add a slack notif / flag that a wait time location was not recognized
            return -1

    def __init__(self, data):
        self._data = data

    def process(self):
        if "error" in self._data:
            return {
                "success": False,
                "result": None,
                "error": self._data["error"]
            }
        if self._data["TIMESTAMP"] == "Invalid date":
            return {
                "success": False,
                "result": None,
                "error": "Invalid date"
            }
        tz = pytz.timezone('America/New_York')
        recent_datetime = tz.localize(datetime.strptime(self._data["TIMESTAMP"], '%Y-%m-%d %I:%M:%S %p'))
        canonical_date = recent_datetime.date()
        block_end_time = recent_datetime.time()
        if recent_datetime.hour < 4:
            # between 12am and 4am associate this with the previous day
            canonical_date = canonical_date - timedelta(days=1)
        num_inserted = 0
        ignored_names = set()
        for place in self._data["UNITS"]:
            internal_id = UpdateTransactionsController.vendor_name_to_internal_id(place["UNIT_NAME"])
            if id < 0:
                ignored_names.add(place["UNIT_NAME"])
            else:
                num_inserted += 1
                try:
                    TransactionHistory.objects.create(id = internal_id, canonical_date = canonical_date, block_end_time = block_end_time, transaction_count=place["CROWD_COUNT"])
                except:
                    num_inserted -= 1
        return {
            "success": True,
            "result": {
                "num_inserted": num_inserted,
                "ignored_names": list(ignored_names)
            },
            "error": None
        }
        
