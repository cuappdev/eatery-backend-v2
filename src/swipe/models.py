from django.db import models
from eatery.models import Eatery
# Create your models here.

class WaitTime(models.Model):
    id = models.AutoField(primary_key=True)
    eatery = models.ForeignKey(Eatery, related_name = "wait_time", on_delete=models.DO_NOTHING, default=0)
    wait_time_high = models.IntegerField()
    wait_time_expected = models.IntegerField()
    wait_time_low = models.IntegerField()
    day = models.TextField(default=0)
    hour = models.IntegerField(default=0)
    trials = models.IntegerField(default = 1)

    def int_to_day(self, i):
        int_to_day = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        return int_to_day[i]
