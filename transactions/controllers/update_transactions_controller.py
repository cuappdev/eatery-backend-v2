from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from datetime import datetime, timedelta, tzinfo
from random import randrange
import pytz

from api.datatype.Eatery import EateryID

from transactions.models import TransactionHistory
class UpdateTransactionsController:

    # Converts the Vendor's name for the eatery into the name stored in our backend
    @staticmethod
    def vendor_name_to_internal_id(vendor_eatery_name):
        vendor_eatery_name = ''.join(c.lower() for c in vendor_eatery_name if c.isalpha())
        if vendor_eatery_name == "bearnecessities":
            return EateryID.BEAR_NECESSITIES
        elif vendor_eatery_name == "northstarmarketplace":
            return EateryID.NORTH_STAR_DINING
        elif vendor_eatery_name == "jansensmarket":
            return EateryID.JANSENS_MARKET
        elif vendor_eatery_name == "stockinghallcafe" or vendor_eatery_name == "stockinghall":
            return EateryID.DAIRY_BAR
        elif vendor_eatery_name == "marthas":
            return EateryID.MARTHAS_CAFE
        elif vendor_eatery_name == "cafejennie":
            return EateryID.CAFE_JENNIE
        elif vendor_eatery_name == "goldiescafe":
            return EateryID.GOLDIES_CAFE
        elif vendor_eatery_name == "alicecookhouse":
            return EateryID.COOK_HOUSE
        elif vendor_eatery_name == "carlbeckerhouse":
            return EateryID.BECKER_HOUSE
        elif vendor_eatery_name == "duffield":
            return EateryID.MATTINS_CAFE
        elif vendor_eatery_name == "greendragon":
            return EateryID.GREEN_DRAGON
        elif vendor_eatery_name == "trillium":
            return EateryID.TRILLIUM
        elif vendor_eatery_name == "olinlibecafe":
            return EateryID.LIBE_CAFE
        elif vendor_eatery_name == "carolscafe":
            return EateryID.CAROLS_CAFE
        elif vendor_eatery_name == "statlerterrace":
            return EateryID.TERRACE
        elif vendor_eatery_name == "busstopbagels":
            return EateryID.BUS_STOP_BAGELS
        elif vendor_eatery_name == "kosher":
            return EateryID.ONE_ZERO_FOUR_WEST
        elif vendor_eatery_name == "jansensatbethehouse":
            return EateryID.BETHE_HOUSE
        elif vendor_eatery_name == "keetonhouse":
            return EateryID.KEETON_HOUSE
        elif vendor_eatery_name == "rpme":
            return EateryID.RPCC
        elif vendor_eatery_name == "rosehouse":
            return EateryID.ROSE_HOUSE
        elif vendor_eatery_name == "risley":
            return EateryID.RISLEY
        elif vendor_eatery_name == "frannysft":
            return EateryID.FRANNYS
        elif vendor_eatery_name == "mccormicks":
            return EateryID.MCCORMICKS
        elif vendor_eatery_name == "sage":
            return EateryID.ATRIUM_CAFE
        elif vendor_eatery_name == "straightmarket":
            return EateryID.STRAIGHT_FROM_THE_MARKET
        elif vendor_eatery_name == "crossingscafe":
            return EateryID.CROSSINGS_CAFE
        elif vendor_eatery_name == "okenshields":
            return EateryID.OKENSHIELDS
        elif vendor_eatery_name == "bigredbarn":
            return EateryID.BIG_RED_BARN
        elif vendor_eatery_name == "rustys":
            return EateryID.RUSTYS
        elif vendor_eatery_name == "manncafe":
            return EateryID.MANN_CAFE
        elif vendor_eatery_name == "statlermacs":
            return EateryID.MACS_CAFE
        else:
            # TODO: Add a slack notif / flag that a wait time location was not recognized
            return None

    def __init__(self, data):
        self._data = data

    def process(self):
        if self._data["TIMESTAMP"] == "Invalid date":
            return 0
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
            internal_id = UpdateTransactionsController.vendor_name_to_internal_id(place["UNIT_NAME"]).value
            if internal_id == None:
                ignored_names.add(place["UNIT_NAME"])
            else:
                num_inserted += 1
                try:
                    TransactionHistory.objects.create(eatery_id = internal_id, canonical_date = canonical_date, block_end_time = block_end_time, transaction_count=place["CROWD_COUNT"])
                except Exception as e:
                    print(e)
                    num_inserted -= 1
        return num_inserted
        
