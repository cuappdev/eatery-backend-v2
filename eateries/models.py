from django.db import models

# Create your models here.
class Eatery(models.Model):
    class Meta:
        unique_together = ('name', 'block_end_time', 'canonical_date')
        indexes = [models.Index(fields = ['canonical_date'])]  
    ud
    canonical_date = models.DateField()
    block_end_time = models.TimeField()
    transaction_count = models.IntegerField()