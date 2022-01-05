from django.db import models

# Create your models here.

# [transaction_count] transactions at [name] in time range [block_end_time - 5 minutes, block_end_time] on [canonical_date]
class TransactionHistory(models.Model):
    class Meta:
        unique_together = ('eatery_id', 'block_end_time', 'canonical_date')
        indexes = [models.Index(fields = ['canonical_date'])]  
    eatery_id = models.IntegerField()
    canonical_date = models.DateField()
    block_end_time = models.TimeField()
    transaction_count = models.IntegerField()