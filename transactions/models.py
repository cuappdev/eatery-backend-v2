from django.db import models

# Create your models here.

class TransactionHistory(models.Model):
    name = models.CharField(max_length=100)
    canonical_date = models.DateField()
    start_timestamp = models.TimeField()
    end_timestamp = models.TimeField()
    transaction_count = models.IntegerField()