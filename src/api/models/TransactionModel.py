from django.db import models
from eatery.models import EateryStore

# [transaction_count] transactions at [name] in time range [block_end_time - 5 minutes, block_end_time] on [canonical_date]


class TransactionHistoryStore(models.Model):
    class Meta:
        unique_together = ('eatery_id', 'block_end_time', 'canonical_date')
        indexes = [models.Index(fields=['canonical_date'])]
    eatery = models.ForeignKey(EateryStore, on_delete=models.DO_NOTHING)
    canonical_date = models.DateField()
    block_end_time = models.TimeField()
    transaction_count = models.IntegerField()
