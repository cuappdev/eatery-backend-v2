from datetime import date, datetime, timedelta

import pytz
from django.db.models import Avg

from api.datatype.Eatery import Eatery, EateryID
from api.datatype.Event import Event
from api.datatype.WaitTime import WaitTime
from api.datatype.WaitTimesDay import WaitTimesDay
from api.dfg.DfgNode import DfgNode
from transactions.models import TransactionHistory

tz = pytz.timezone('America/New_York')

class WaitTimes(DfgNode):

    def __init__(self, eatery_id: EateryID, cache):
        self.eatery_id = eatery_id
        self.cache = cache

    def __call__(self, *args, **kwargs) -> list[Eatery]:
        if "transactions" not in self.cache:
            transactions = {}
            date = kwargs.get("start")
            while date <= kwargs.get("end"):
                transactions[date] = []
                past_days = []
                for i in range(1, 13):
                    past_days.append(date - timedelta(days=7*i))
                transaction_avg_counts = TransactionHistory.objects.filter(canonical_date__in=past_days) \
                    .values("eatery_id", "block_end_time") \
                    .annotate(transaction_avg=Avg("transaction_count"))
                for unit in transaction_avg_counts:
                    transactions[date].append(unit)
                date += timedelta(days=1)
            self.cache["transactions"] = transactions
        
        eatery_wait_times = []
        for date in self.cache["transactions"]:
            eatery_transaction_avgs = [transaction_avg for transaction_avg in self.cache["transactions"][date] if transaction_avg["eatery_id"] == self.eatery_id.value]
            eatery_wait_times.append(WaitTimes.generate_eatery_wait_times_by_day(self.eatery_id, date, eatery_transaction_avgs))

        return eatery_wait_times

    # Expected amount of time (in seconds) for the length of the line to decrease by 1 person
    # Returns [lower, expected, upper]
    @staticmethod
    def line_decrease_by_one_time(eatery_id: EateryID) -> list[int]:
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

    # Expected amount of time (in seconds) for a person to get food, assuming an empty eatery, not including the
    # amount of time to check out Returns [lower, expected, upper]
    @staticmethod
    def base_time_to_get_food(eatery_id: EateryID) -> list[int]:
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
        eatery_id: EateryID,
        date: date,
        transactions: list
    ) -> WaitTimesDay:
        wait_times_data = []
        customers_waiting_in_line = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        for index in reversed(range(0, len(transactions))):
            base_times = WaitTimes.base_time_to_get_food(eatery_id)
            line_decrease_times = WaitTimes.line_decrease_by_one_time(eatery_id)
            # we assume all the guests in this transaction bucket showed up [how_long_ago_guest_arrival] minutes ago
            how_long_ago_guest_arrival = base_times[1] + line_decrease_times[1] * transactions[index]["transaction_avg"]
            prev_bucket_guest_arrival = int(how_long_ago_guest_arrival // (5 * 60))
            if prev_bucket_guest_arrival > 9:
                # TODO: Send a slack error here instead
                print("Fatal Wait Times Error - prev_bucket_guest_arrival far too large.")
            else:
                customers_waiting_in_line[prev_bucket_guest_arrival] += transactions[index]["transaction_avg"]
                num_customers = customers_waiting_in_line.pop(0)
                wait_time_low = int(base_times[0] + line_decrease_times[0] * num_customers)
                wait_time_expected = int(base_times[1] + line_decrease_times[1] * num_customers)
                wait_time_high = int(base_times[2] + line_decrease_times[2] * num_customers)

                customers_waiting_in_line.append(0.0)
                block_end_time = transactions[index]['block_end_time']
                timestamp = int(Event.combined_timestamp(date, block_end_time, tz) - 5 * 60 / 2)
                wait_times_data.insert(0, WaitTime(
                    timestamp=timestamp,
                    wait_time_low=wait_time_low,
                    wait_time_expected=wait_time_expected,
                    wait_time_high=wait_time_high
                ))

        return WaitTimesDay(canonical_date=date, data=wait_times_data)


    def description(self):
        return "WaitTimes"
