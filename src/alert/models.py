from django.db import models
from eatery.models import Eatery


class Alert(models.Model):
    id = models.IntegerField(primary_key=True)
    eatery = models.ForeignKey(Eatery, on_delete=models.DO_NOTHING)
    description = models.CharField(max_length = 250)
    start_timestamp = models.IntegerField()
    end_timestamp = models.IntegerField()


def __str__(self):
      return self.description