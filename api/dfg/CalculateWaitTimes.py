from api.dfg.DfgNode import DfgNode
from transactions.models import TransactionHistory
from transactions.serializers import TransactionHistorySerializer
from ..datatype.EateryResult import EateryResult
from ..datatype.WaitTime import WaitTime
from ..datatype.WaitTimesByDay import WaitTimesByDay

from django.db.models import Avg
from datetime import datetime, timedelta, tzinfo
import pytz

class CalculateWaitTimes(DfgNode):

    def __init__(self, child: DfgNode):
        self.child = child

    def __call__(self, *args, **kwargs) -> list[EateryResult]:
        eatery_results = []
        wait_times = {} # [date]: {[eateryname]: list[WaitTime]}
        past_days = []
        date = kwargs.get("start")
        while date <= kwargs.get("end"):
            # We only calculate the wait times for this first day
            eatery_waits_on_date = {}
            for i in range(1, 13):
                # Look at the last 13 weeks, for each block_end_time for the same day of week, average together the transaction_count
                past_day = date - timedelta(days = 7 * i)
                past_days.append(past_day)
            transaction_avg_counts = TransactionHistory.objects.filter(canonical_date__in=past_days).values("name", "block_end_time").annotate(transaction_avg=Avg("transaction_count"))
            for unit in transaction_avg_counts:
                transaction_history = TransactionHistorySerializer(unit)
                eatery_name = transaction_history.data['name']
                block_end_time = datetime.strptime(transaction_history.data['block_end_time'], '%H:%M:%S').time()
                block_end_timestamp = CalculateWaitTimes.timestamp_combined(date, block_end_time)
                transaction_average = transaction_history.data["transaction_avg"]
                if eatery_name not in eatery_waits_on_date:
                    eatery_waits_on_date[eatery_name] = []
                eatery_waits_on_date[eatery_name].append(WaitTime(block_end_timestamp, transaction_average))
            wait_times[date] = eatery_waits_on_date
            date += timedelta(days=1)
        for eatery in self.child(*args, **kwargs):
            eatery_wait_times_by_day = []
            for date in wait_times:
                if eatery.name in wait_times[date]:
                    eatery_wait_times_by_day.append(WaitTimesByDay(date, wait_times[date][eatery.name]))
            eatery_results.append(EateryResult(eatery, eatery_wait_times_by_day))

        return eatery_results

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
