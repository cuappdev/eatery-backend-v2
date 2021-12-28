from django.db import models

# Create your models here.

# [transaction_count] transactions at [name] in time range [block_end_time - 5 minutes, block_end_time] on [canonical_date]
class TransactionHistory(models.Model):
    class Meta:
        unique_together = ('name', 'block_end_time', 'canonical_date')
        indexes = [models.Index(fields = ['canonical_date'])]  
    name = models.CharField(max_length=100)
    canonical_date = models.DateField()
    block_end_time = models.TimeField()
    transaction_count = models.IntegerField()