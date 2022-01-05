from typing import Mapping
from django.db.models import Avg
from datetime import date, datetime, timedelta
import pytz

from api.datatype.Eatery import Eatery, EateryID
from api.datatype.WaitTimesDay import WaitTimesDay
from api.datatype.WaitTime import WaitTime

from api.dfg.DfgNode import DfgNode
from transactions.models import TransactionHistory
from transactions.serializers import TransactionHistorySerializer

class WaitTimes(DfgNode):

    def __call__(self, *args, **kwargs) -> list[Eatery]:
        transactions_by_date = {}
        past_days = []
        date = kwargs.get("start")
        eatery_ids = set()
        while date <= kwargs.get("end"):
            # We only calculate the wait times for this first day
            transactions_on_date = {}
            for i in range(1, 13):
                # Look at the last 13 weeks, for each block_end_time for the same day of week, average together the transaction_count
                past_day = date - timedelta(days = 7 * i)
                past_days.append(past_day)
            transaction_avg_counts = TransactionHistory.objects.filter(canonical_date__in=past_days) \
                .values("eatery_id", "block_end_time") \
                .annotate(transaction_avg=Avg("transaction_count"))
            for unit in transaction_avg_counts:
                transaction_history = TransactionHistorySerializer(unit)
                if transaction_history.data['eatery_id'] != 0:
                    eatery_id = EateryID(transaction_history.data['eatery_id'])
                    eatery_ids.add(eatery_id)
                    if eatery_id not in transactions_on_date:
                        transactions_on_date[eatery_id] = []
                    transactions_on_date[eatery_id].append(transaction_history)
            transactions_by_date[date] = transactions_on_date
            date += timedelta(days=1)
        
        eateries = []
        for eatery_id in eatery_ids:
            eatery_wait_times_by_day = []
            for date in transactions_by_date:
                if eatery_id in transactions_by_date[date]:
                    eatery_wait_times_by_day.append(WaitTimes.generate_eatery_wait_times_by_day(eatery_id, date, transactions_by_date[date][eatery_id]))
            eateries.append(
                Eatery(
                    id=eatery_id, 
                    wait_times = eatery_wait_times_by_day
                )
            )
        return eateries

    # Expected amount of time (in seconds) for the length of the line to decrease by 1 person
    # Returns [lower, expected, upper]
    @staticmethod
    def line_decrease_by_one_time(eatery_id: EateryID) -> float:
        if eatery_id == EateryID.MACS_CAFE:
            return [24, 27, 30]
        elif eatery_id == EateryID.MATTINS_CAFE:
            return [9, 15, 21]
        elif eatery_id == EateryID.TERRACE:
            return [15, 27, 36]
        elif eatery_id == EateryID.OKENSHIELDS:
            return [4, 8, 12]
        else:
            return [18, 21, 24]
    
    # Expected amount of time (in seconds) for a person to get food, assuming an empty eatery, not including the amount of time to check out
    # Returns [lower, expected, upper]
    @staticmethod
    def base_time_to_get_food(eatery_id: int) -> float:
        if eatery_id == EateryID.MACS_CAFE:
            return [240, 300, 360]
        elif eatery_id == EateryID.MATTINS_CAFE:
            return [150, 210, 270]
        elif eatery_id == EateryID.TERRACE:
            return [180, 300, 420]
        elif eatery_id == EateryID.OKENSHIELDS:
            return [80, 120, 180]
        else:
            return [180, 240, 300]

    @staticmethod
    def generate_eatery_wait_times_by_day(
        eatery_id: int, 
        date: date, 
        transactions: list[TransactionHistorySerializer]
    ) -> WaitTimesDay:
        wait_times_data = []
        customers_waiting_in_line = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        for index in reversed(range(0, len(transactions))):
            base_times = WaitTimes.base_time_to_get_food(eatery_id)
            line_decrease_times = WaitTimes.line_decrease_by_one_time(eatery_id)
            # we assume all the guests in this transaction bucket showed up [how_long_ago_guest_arrival] minutes ago
            how_long_ago_guest_arrival = base_times[1] + line_decrease_times[1] * transactions[index].data["transaction_avg"]
            prev_bucket_guest_arrival = int(how_long_ago_guest_arrival // (5 * 60))
            if prev_bucket_guest_arrival > 9:
                # TODO: Send a slack error here instead
                print("Fatal Wait Times Error - prev_bucket_guest_arrival far too large.")
            else:
                customers_waiting_in_line[prev_bucket_guest_arrival] += transactions[index].data["transaction_avg"]
                num_customers = customers_waiting_in_line.pop(0)
                wait_time_low = int(base_times[0] + line_decrease_times[0] * num_customers)
                wait_time_expected = int(base_times[1] + line_decrease_times[1] * num_customers)
                wait_time_high = int(base_times[2] + line_decrease_times[2] * num_customers)

                customers_waiting_in_line.append(0.0)
                block_end_time = datetime.strptime(transactions[index].data['block_end_time'], '%H:%M:%S').time()
                timestamp = int(WaitTimes.timestamp_combined(date, block_end_time) - 5 * 60 / 2)
                wait_times_data.insert(0, WaitTime(
                        timestamp=timestamp, 
                        wait_time_low = wait_time_low,
                        wait_time_expected= wait_time_expected,
                        wait_time_high = wait_time_high))
                
        return WaitTimesDay(canonical_date = date, data = wait_times_data)

    @staticmethod
    def timestamp_combined(date: datetime.date, time: datetime.time):
        """
        Returns the Unix (UTC) timestamp of the combined (date, time) in the
        New York timezone.
        """

        tz = pytz.timezone('America/New_York')
        return int(tz.localize(datetime.combine(date, time)).timestamp())

    def description(self):
        return "WaitTimes"
