from typing import Mapping
from django.db.models import Avg
from datetime import date,  timedelta

from api.dfg.DfgNode import DfgNode
from transactions.models import TransactionHistory
from transactions.serializers import TransactionHistorySerializer

class FetchTransactionCounts(DfgNode):

    def __call__(self, *args, **kwargs) -> Mapping[date, Mapping[str, list[TransactionHistory]]]:
        transactions_by_date = {}
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
        
        return transactions_by_date
        
    def description(self):
        return "FetchTransactionCounts"
