# takes in api_data, google_sheets data, and stubs, and generates a list[Eatery]

from typing import Mapping
from datetime import date, datetime
import pytz

from api.dfg.DfgNode import DfgNode
from api.dfg.assembly.datatype.Eatery import Eatery
from api.dfg.DfgNode import DfgNode
from api.dfg.waittimes.datatype.EateryWithWaitTimes import EateryWithWaitTimes
from api.dfg.waittimes.datatype.WaitTime import WaitTime
from api.dfg.waittimes.datatype.WaitTimesByDay import WaitTimesByDay

from transactions.serializers import TransactionHistorySerializer


class AddWaitTimesToEateries(DfgNode):

    def __init__(self, eateries: DfgNode, transaction_counts: DfgNode):
        self.eateries = eateries
        self.transaction_counts = transaction_counts

    def __call__(self, *args, **kwargs):
        results = []
        transactions_by_date = self.transaction_counts(*args, **kwargs)

        for eatery in self.eateries(*args, **kwargs):
           results.append(AddWaitTimesToEateries.generate_eatery_result(eatery, transactions_by_date))

        return results


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
        elif eatery_name == "Okenshields":
            return [4, 8, 12]
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
        elif eatery_name == "Okenshields":
            return [80, 120, 180]
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
            base_times = AddWaitTimesToEateries.BASE_TIME_TO_GET_FOOD(eatery.name)
            line_decrease_times = AddWaitTimesToEateries.LINE_DECREASE_BY_ONE_TIME(eatery.name)
            # we assume all the guests in this transaction bucket showed up [how_long_ago_guest_arrival] minutes ago
            how_long_ago_guest_arrival = base_times[1] + line_decrease_times[1] * transactions[index].data["transaction_avg"]
            prev_bucket_guest_arrival = int(how_long_ago_guest_arrival // (5 * 60))
            if prev_bucket_guest_arrival > 9:
                # TODO: Send a slack error here instead
                print(how_long_ago_guest_arrival)
                print(date)
                print(transactions[index].data)
                print("Fatal Wait Times Error - prev_bucket_guest_arrival far too large.")
            else:
                customers_waiting_in_line[prev_bucket_guest_arrival] += transactions[index].data["transaction_avg"]
                num_customers = customers_waiting_in_line.pop(0)
                wait_time_low = int(base_times[0] + line_decrease_times[0] * num_customers)
                wait_time_expected = int(base_times[1] + line_decrease_times[1] * num_customers)
                wait_time_high = int(base_times[2] + line_decrease_times[2] * num_customers)

                customers_waiting_in_line.append(0.0)
                block_end_time = datetime.strptime(transactions[index].data['block_end_time'], '%H:%M:%S').time()
                timestamp = int(AddWaitTimesToEateries.timestamp_combined(date, block_end_time) - 5 * 60 / 2)
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
    ) -> EateryWithWaitTimes:
        eatery_wait_times_by_day = []
        for date in transactions_by_date:
            if eatery.name in transactions_by_date[date]:
                eatery_wait_times_by_day.append(AddWaitTimesToEateries.generate_eatery_wait_times_by_day(eatery, date, transactions_by_date[date][eatery.name]))
        return EateryWithWaitTimes(eatery, eatery_wait_times_by_day)

    @staticmethod
    def timestamp_combined(date: datetime.date, time: datetime.time):
        """
        Returns the Unix (UTC) timestamp of the combined (date, time) in the
        New York timezone.
        """

        tz = pytz.timezone('America/New_York')
        return int(tz.localize(datetime.combine(date, time)).timestamp())

    def description(self):
        return "AddWaitTimesToEateries"
