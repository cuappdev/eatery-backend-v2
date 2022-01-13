from django.db import models
from api.models.EateryModel import EateryStore
from api.models.MenuModel import MenuStore

class EventDescription(models.TextChoices):
    BREAKFAST = 'Breakfast'
    BRUNCH = 'Brunch'
    LUNCH = 'Lunch'
    DINNER = 'Dinner'
    GENERAL = 'General'

class EventSchedule(models.Model):
    id = models.IntegerField(primary_key=True)
    eatery = models.ForeignKey(EateryStore, on_delete=models.DO_NOTHING)
    class Meta:
        abstract=True

class DayOfWeekEventSchedule(EventSchedule):
     
    class DayOfTheWeek(models.TextChoices):
        MONDAY = 'Monday'
        TUESDAY = 'Tuesday'
        WEDNESDAY = 'Wednesday'
        THURSDAY = 'Thursday'
        FRIDAY = 'Friday'
        SATURDAY = 'Saturday'
        SUNDAY = 'Sunday'

    event_description = models.CharField(choices=EventDescription.choices, max_length = 10)
    menu= models.ForeignKey(MenuStore, on_delete=models.DO_NOTHING)
    day_of_week = models.CharField(choices = DayOfTheWeek.choices, max_length=10)
    start = models.TimeField()
    end = models.TimeField()
    class Meta:
        unique_together = ('eatery', 'day_of_week', 'event_description')
    

class DateEventSchedule(EventSchedule):
    event_description = models.CharField(choices=EventDescription.choices, max_length = 10)
    menu = models.ForeignKey(MenuStore, on_delete=models.DO_NOTHING)
    canonical_date = models.DateField()
    start_timestamp = models.IntegerField()
    end_timestamp = models.IntegerField()

class ClosedEventSchedule(EventSchedule):
    event_description = models.CharField(choices=EventDescription.choices, max_length = 10)
    canonical_date = models.DateField()
