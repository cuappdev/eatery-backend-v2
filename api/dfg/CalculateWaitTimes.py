from api.dfg.DfgNode import DfgNode
from transactions.models import TransactionHistory
from transactions.serializers import TransactionHistorySerializer

import datetime

class CalculateWaitTimes(DfgNode):

    def __init__(self, child: DfgNode):
        self.child = child

    def __call__(self, *args, **kwargs):
        eateries_with_wait_times = []
        past_days = []
        # kwargs.get("start")
        for i in range(1, 13):
            past_day = datetime.date.today() - datetime.timedelta(days = 7 * i)
            past_days.append(past_day)

        transaction_data = TransactionHistory.objects.filter(canonical_date__in=past_days)
        # print(len(transaction_data))
        # print('--------------------')
        # print(transaction_data)
        for eatery in self.child(*args, **kwargs):
            eateries_with_wait_times.append(eatery)

        return eateries_with_wait_times

    def children(self):
        return [self.child]

    def description(self):
        return "CalculateWaitTimes"
