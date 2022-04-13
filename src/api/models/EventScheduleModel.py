from enum import Enum

from api.models.EateryModel import EateryStore
from api.models.MenuModel import MenuStore
from django.core.validators import validate_comma_separated_integer_list
from django.db import models


class EventDescription(models.TextChoices):
    BREAKFAST = "Breakfast"
    BRUNCH = "Brunch"
    LUNCH = "Lunch"
    DINNER = "Dinner"
    GENERAL = "General"


class EventSchedule(models.Model):
    id = models.IntegerField(primary_key=True)
    eatery = models.ForeignKey(EateryStore, on_delete=models.DO_NOTHING)

    class Meta:
        abstract = True


class RepeatingEventSchedule(EventSchedule):

    event_description = models.CharField(
        choices=EventDescription.choices, max_length=10
    )
    menu = models.ForeignKey(MenuStore, on_delete=models.DO_NOTHING)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    repeat_interval = models.IntegerField()
    offset_lst = models.CharField(
        validators=[validate_comma_separated_integer_list], max_length=100
    )

    class Meta:
        unique_together = ("eatery", "event_description")


class ExceptionType(models.TextChoices):
    CLOSED = "closed"
    MODIFIED = "modified"


class ScheduleException(models.Model):
    id = models.IntegerField(primary_key=True)
    parent = models.ForeignKey(RepeatingEventSchedule, on_delete=models.DO_NOTHING)
    date = models.DateField()
    exception_type = models.CharField(max_length=10, choices=ExceptionType.choices)
    start_time = models.DateField(blank=True, null=True)
    end_time = models.DateField(blank=True, null=True)
