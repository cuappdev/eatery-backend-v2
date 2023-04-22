from django.db import models
from eatery.models import Eatery
from django.contrib.postgres.fields import ArrayField
# Create your models here.

class Day(models.TextChoices):
    SUN = "Sunday"
    MON = "Monday"
    TUES = "Tuesday"
    WED = "Wednesday"
    THURS = "Thursday"
    FRI = "Friday"
    SAT = "Saturday"

class WaitTime(models.Model):
    id = models.AutoField(primary_key=True)
    canonical_date = models.IntegerField()
    eatery = models.ForeignKey(Eatery, related_name = "wait_time", on_delete=models.DO_NOTHING)
    wait_time_high = models.IntegerField()
    wait_time_expected = models.IntegerField()
    wait_time_low = models.IntegerField()
    day = models.TextField(
        choices=Day.choices, blank=True, null = True)
    hour = models.IntegerField()
