from django.db import models

# Create your models here.

# [transaction_count] transactions at [name] in time range [timestamp - 5 minutes, timestamp] on [canonical_date]
class TransactionHistory(models.Model):
    class Meta:
        unique_together = ('name', 'timestamp', 'canonical_date')
        indexes = [models.Index(fields = ['canonical_date'])]  
    name = models.CharField(max_length=100)
    canonical_date = models.DateField()
    timestamp = models.TimeField()
    transaction_count = models.IntegerField()