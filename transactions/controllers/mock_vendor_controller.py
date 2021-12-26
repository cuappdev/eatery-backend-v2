from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from datetime import datetime
from pytz import timezone
from random import randrange

class MockVendorController:
    def process(self):
        tz = timezone("EST")
        now = datetime.now(tz)
        recent_timestamp = datetime(now.year, now.month, now.day, now.hour, now.minute - now.minute%5, 0, 0)
        places = ['Bear Necessities', 'North Star Marketplace', "Jansen's Market", 'StockingHallCafe', 'Marthas', 'Cafe Jennie', "Goldie's Cafe", 'Alice Cook House', 'Carl Becker House', 'Duffield', 'Green Dragon', 'Trillium', 'Olin Libe Cafe',  'Carols Cafe', 'Statler Terrace', 'Bus Stop Bagels', 'Stocking Hall', 'Kosher', 'Jansens at Bethe House', 'Keeton House', 'RPME', 'Rose House', 'Catering', 'DIN Special Event', 'Risley', "Franny's FT", 'HA3350', "McCormick's", 'Statler Banfi', "Statler Banfi's", 'Statler Regent', 'Sage', 'Straight Market', 'Concession Suite', 'Crossings Cafe', 'Okenshields', 'Big Red Barn', 'Rustys', 'Mann Cafe', 'Statler Macs', 'Morrison']
        units = []
        for place in places:
            crowd_count = randrange(6)
            if crowd_count > 0:
                units.append({
                    "UNIT_NAME": place,
                    "CROWD_COUNT": crowd_count
                })

        return JsonResponse({
            "TIMESTAMP": recent_timestamp.strftime('%Y-%m-%d %I:%M:%S %p'),
            "LOOK_BACK_MINUTES": 5,
            "UNITS": units
        })
