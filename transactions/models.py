from django.db import models

# Create your models here.

# [transaction_count] transactions at [name] in time range [timestamp - 5 minutes, timestamp] on [canonical_date]
class TransactionHistory(models.Model):
    class Meta:
        unique_together = ('name', 'timestamp', 'canonical_date')
        # idea is when fetching wait time for [name] in between [timestamp - 5, timestamp], we can look at the last 2 weeks of data for that [name, timestamp] pair
        indexes = [models.Index(fields = ['name', 'timestamp', 'canonical_date'])]  
    name = models.CharField(max_length=100)
    canonical_date = models.DateField()
    timestamp = models.TimeField()
    transaction_count = models.IntegerField()