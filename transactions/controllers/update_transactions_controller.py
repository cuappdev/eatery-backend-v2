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
    def eatery_name(vendor_eatery_name):
        vendor_eatery_name = ''.join(c.lower() for c in vendor_eatery_name if c.isalpha())
        if vendor_eatery_name == "bearnecessities":
            return "Bear Necessities Grill & C-Store"
        elif vendor_eatery_name == "northstarmarketplace":
            return "North Star Dining Room"
        elif vendor_eatery_name == "jansensmarket":
            return "Jansen's Market"
        elif vendor_eatery_name == "stockinghallcafe" or vendor_eatery_name == "stockinghall":
            return "Cornell Dairy Bar"
        elif vendor_eatery_name == "marthas":
            return "Martha's Café"
        elif vendor_eatery_name == "cafejennie":
            return "Café Jennie"
        elif vendor_eatery_name == "goldiescafe":
            return "Goldie's Café"
        elif vendor_eatery_name == "alicecookhouse":
            return "Cook House Dining Room"
        elif vendor_eatery_name == "carlbeckerhouse":
            return "Becker House Dining Room"
        elif vendor_eatery_name == "duffield":
            return "Mattin's Café"
        elif vendor_eatery_name == "greendragon":
            return "Green Dragon"
        elif vendor_eatery_name == "trillium":
            return "Trillium"
        elif vendor_eatery_name == "olinlibecafe":
            return "Amit Bhatia Libe Café"
        elif vendor_eatery_name == "carolscafe":
            return "Carol's Café"
        elif vendor_eatery_name == "statlerterrace":
            return "Terrace Restaurant"
        elif vendor_eatery_name == "busstopbagels":
            return "Bus Stop Bagels"
        elif vendor_eatery_name == "kosher":
            return "104West!"
        elif vendor_eatery_name == "jansensatbethehouse":
            return "Jansen's Dining Room at Bethe House"
        elif vendor_eatery_name == "keetonhouse":
            return "Keeton House Dining Room"
        elif vendor_eatery_name == "rpme":
            return "Robert Purcell Marketplace Eatery"
        elif vendor_eatery_name == "rosehouse":
            return "Rose House Dining Room"
        elif vendor_eatery_name == "risley":
            return "Risley Dining Room"
        elif vendor_eatery_name == "frannysft":
            return "Franny's"
        elif vendor_eatery_name == "mccormicks":
            return "McCormick's at Moakley House"
        elif vendor_eatery_name == "sage":
            return "Atrium Café"
        elif vendor_eatery_name == "straightmarket":
            return "Straight from the Market"
        elif vendor_eatery_name == "crossingscafe":
            return "Crossings Café"
        elif vendor_eatery_name == "okenshields":
            return "Okenshields"
        elif vendor_eatery_name == "bigredbarn":
            return "Big Red Barn"
        elif vendor_eatery_name == "rustys":
            return "Rusty's"
        elif vendor_eatery_name == "manncafe":
            return "Mann Café"
        elif vendor_eatery_name == "statlermacs":
            return "Mac's Café"
        else:
            # TODO: Add a slack notif / flag that a wait time location was not recognized
            return ""

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
            name = UpdateTransactionsController.eatery_name(place["UNIT_NAME"])
            if len(name) == 0:
                ignored_names.add(place["UNIT_NAME"])
            else:
                num_inserted += 1
                try:
                    TransactionHistory.objects.create(name = name, canonical_date = canonical_date, block_end_time = block_end_time, transaction_count=place["CROWD_COUNT"])
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
        
