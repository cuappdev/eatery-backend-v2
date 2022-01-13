from datetime import datetime, timedelta
import pytz

from api.models import TransactionHistoryStore
from api.util.constants import vendor_name_to_internal_id

class CreateTransactionController:

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
            # between 12am and 4am associate this transaction with the previous day
            canonical_date = canonical_date - timedelta(days=1)
        num_inserted = 0
        ignored_names = set()
        for place in self._data["UNITS"]:
            internal_id = vendor_name_to_internal_id(place["UNIT_NAME"]).value
            if internal_id == None:
                ignored_names.add(place["UNIT_NAME"])
            else:
                num_inserted += 1
                try:
                    TransactionHistoryStore.objects.create(
                        eatery_id = internal_id, 
                        canonical_date = canonical_date, 
                        block_end_time = block_end_time, 
                        transaction_count=place["CROWD_COUNT"]
                    )
                except Exception as e:
                    # print(e)
                    num_inserted -= 1
        return num_inserted
        
