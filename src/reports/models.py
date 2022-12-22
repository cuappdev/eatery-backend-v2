from django.db import models
from eatery.models import Eatery


class ReportStore(models.Model):
    eatery = models.ForeignKey(Eatery, on_delete=models.DO_NOTHING, null=True)
    type = models.CharField(max_length=200)
    content = models.TextField()
    created_timestamp = models.IntegerField()
