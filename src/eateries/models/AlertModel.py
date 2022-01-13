from django.db import models
from eateries.models.EateryModel import EateryStore

class AlertStore(models.Model):
    id = models.IntegerField(primary_key=True)
    eatery = models.ForeignKey(EateryStore, on_delete=models.DO_NOTHING)
    description = models.CharField(max_length = 250)
    start_timestamp = models.IntegerField()
    end_timestamp = models.IntegerField()
