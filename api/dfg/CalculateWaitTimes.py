from typing import Mapping
from api.datatype.Eatery import Eatery
from api.dfg.DfgNode import DfgNode
from transactions.models import TransactionHistory
from transactions.serializers import TransactionHistorySerializer
from ..datatype.EateryResult import EateryResult
from ..datatype.WaitTime import WaitTime
from ..datatype.WaitTimesByDay import WaitTimesByDay

from django.db.models import Avg
from datetime import date, datetime, timedelta, tzinfo
import pytz
class CalculateWaitTimes(DfgNode):

    def __init__(self, child: DfgNode):
        self.child = child

    def __call__(self, *args, **kwargs) -> list[EateryResult]:
        eatery_results = []
        transactions_by_date = {} # [date]: {[eateryname]: list[TransactionHistory]}
        past_days = []
        date = kwargs.get("start")
        while date <= kwargs.get("end"):
            # We only calculate the wait times for this first day
            transactions_on_date = {}
            for i in range(1, 13):
                # Look at the last 13 weeks, for each block_end_time for the same day of week, average together the transaction_count
                past_day = date - timedelta(days = 7 * i)
                past_days.append(past_day)
            transaction_avg_counts = TransactionHistory.objects.filter(canonical_date__in=past_days) \
                .values("name", "block_end_time") \
                .annotate(transaction_avg=Avg("transaction_count"))
            for unit in transaction_avg_counts:
                transaction_history = TransactionHistorySerializer(unit)
                eatery_name = transaction_history.data['name']
                if eatery_name not in transactions_on_date:
                    transactions_on_date[eatery_name] = []
                transactions_on_date[eatery_name].append(transaction_history)
            transactions_by_date[date] = transactions_on_date
            date += timedelta(days=1)
        for eatery in self.child(*args, **kwargs):
            eatery_results.append(CalculateWaitTimes.generate_eatery_result(eatery, transactions_by_date))

        return eatery_results

    # Expected amount of time (in seconds) for the length of the line to decrease by 1 person
    # Returns [lower, expected, upper]
    @staticmethod
    def LINE_DECREASE_BY_ONE_TIME(eatery_name: str) -> float:
        # TODO: Move these hardcoded names into a string file
        if eatery_name == "Mac's Café": 
            return [24, 27, 30]
        elif eatery_name == "Mattin's Café":
            return [9, 15, 21]
        elif eatery_name == "Terrace Restaurant":
            return [15, 27, 36]
        else:
            return [18, 21, 24]
    
    # Expected amount of time (in seconds) for a person to get food, assuming an empty eatery, not including the amount of time to check out
    # Returns [lower, expected, upper]
    @staticmethod
    def BASE_TIME_TO_GET_FOOD(eatery_name: str) -> float:
        if eatery_name == "Mac's Café":
            return [240, 300, 360]
        elif eatery_name == "Mattin's Café":
            return [150, 210, 270]
        elif eatery_name == "Terrace Restaurant":
            return [180, 300, 420]
        else:
            return [180, 240, 300]

    @staticmethod
    def generate_eatery_wait_times_by_day(
        eatery: Eatery, 
        date: date, 
        transactions: list[TransactionHistorySerializer]
    ) -> WaitTimesByDay:
        wait_times = []
        customers_waiting_in_line = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        for index in reversed(range(0, len(transactions))):
            base_times = CalculateWaitTimes.BASE_TIME_TO_GET_FOOD(eatery.name)
            line_decrease_times = CalculateWaitTimes.LINE_DECREASE_BY_ONE_TIME(eatery.name)
            # we assume all the guests in this transaction bucket showed up [how_long_ago_guest_arrival] minutes ago
            how_long_ago_guest_arrival = base_times[1] + line_decrease_times[1] * transactions[index].data["transaction_avg"]
            prev_bucket_guest_arrival = int(how_long_ago_guest_arrival // (5 * 60))
            if prev_bucket_guest_arrival > 9:
                print("Fatal Wait Times Error - prev_bucket_guest_arrival far too large.")
            else:
                customers_waiting_in_line[prev_bucket_guest_arrival] += transactions[index].data["transaction_avg"]
                num_customers = customers_waiting_in_line.pop(0)
                wait_time_low = int(base_times[0] + line_decrease_times[0] * num_customers)
                wait_time_expected = int(base_times[1] + line_decrease_times[1] * num_customers)
                wait_time_high = int(base_times[2] + line_decrease_times[2] * num_customers)

                customers_waiting_in_line.append(0.0)
                block_end_time = datetime.strptime(transactions[index].data['block_end_time'], '%H:%M:%S').time()
                timestamp = int(CalculateWaitTimes.timestamp_combined(date, block_end_time) - 5 * 60 / 2)
                if any([timestamp in event for event in eatery.events()]):
                    wait_times.insert(0, WaitTime(
                            timestamp=timestamp, 
                            wait_time_low = wait_time_low,
                            wait_time_expected= wait_time_expected,
                            wait_time_high = wait_time_high))
                
        return WaitTimesByDay(date, wait_times)

    @staticmethod
    def generate_eatery_result(
        eatery: Eatery, 
        transactions_by_date: Mapping[date, Mapping[str, list[TransactionHistorySerializer]]]
    ) -> EateryResult:
        eatery_wait_times_by_day = []
        for date in transactions_by_date:
            if eatery.name in transactions_by_date[date]:
                eatery_wait_times_by_day.append(CalculateWaitTimes.generate_eatery_wait_times_by_day(eatery, date, transactions_by_date[date][eatery.name]))
        return EateryResult(eatery, eatery_wait_times_by_day)

    @staticmethod
    def timestamp_combined(date: datetime.date, time: datetime.time):
        """
        Returns the Unix (UTC) timestamp of the combined (date, time) in the
        New York timezone.
        """

        tz = pytz.timezone('America/New_York')
        return int(tz.localize(datetime.combine(date, time)).timestamp())

    def children(self):
        return [self.child]

    def description(self):
        return "CalculateWaitTimes"
