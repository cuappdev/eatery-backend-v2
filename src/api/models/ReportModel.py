from eatery.models import EateryStore
from django.db import models


class ReportStore(models.Model):
    eatery = models.ForeignKey(EateryStore, on_delete=models.DO_NOTHING, null=True)
    type = models.CharField(max_length=200)
    content = models.TextField()
    created_timestamp = models.IntegerField()
