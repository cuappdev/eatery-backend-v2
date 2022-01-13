from django.db import models
from eateries.models.EateryModel import EateryStore

class ReportStore(models.Model):
    eatery = models.ForeignKey(EateryStore, on_delete=models.DO_NOTHING)
    type = models.CharField(max_length=200)
    content = models.TextField()
    created_timestamp = models.IntegerField()