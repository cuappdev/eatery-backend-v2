from django.db import models
from django.core.validators import validate_comma_separated_integer_list
from api.models.EateryModel import EateryStore
from api.models.MenuModel import MenuStore


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


class DateEventSchedule(EventSchedule):
    event_description = models.CharField(
        choices=EventDescription.choices, max_length=10
    )
    menu = models.ForeignKey(MenuStore, on_delete=models.DO_NOTHING)
    canonical_date = models.DateField()
    start_timestamp = models.IntegerField()
    end_timestamp = models.IntegerField()


class ClosedEventSchedule(EventSchedule):
    event_description = models.CharField(
        choices=EventDescription.choices, max_length=10
    )
    canonical_date = models.DateField()
