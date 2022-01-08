from django.db import models
from datetime import datetime
class EateryStore(models.Model):
    class CampusArea(models.TextChoices):
        WEST = 'WST', 'West'
        NORTH = 'NRTH', 'North'
        CENTRAL = 'CNTRL', 'Central'
        COLLEGETOWN = 'CTWN', 'Collegetown'
        NONE = 'NN', ''

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40, blank=True)
    menu_summary = models.CharField(max_length = 60, blank=True)
    image_url = models.URLField(blank=True)
    location = models.CharField(max_length=30, blank=True)
    campus_area = models.CharField(max_length=5, choices=CampusArea.choices, default=CampusArea.NONE, blank=True)
    online_order = models.BooleanField(null = True, blank=True)
    online_order_url = models.URLField(blank=True)
    latitude = models.FloatField(null = True, blank=True)
    longitude = models.FloatField(null = True, blank=True)
    payment_accepts_meal_swipes = models.BooleanField(null = True, blank=True)
    payment_accepts_brbs = models.BooleanField(null = True, blank=True)
    payment_accepts_cash = models.BooleanField(null = True, blank=True)

class ExceptionStore(models.Model):
    eatery_id = models.ForeignKey(EateryStore, on_delete=models.DO_NOTHING)
    description = models.CharField(max_length = 250)
    start_timestamp = models.DateTimeField()
    end_timestamp = models.DateTimeField()

class MenuStore(models.Model):
    eatery_id = models.ForeignKey(EateryStore, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length = 40)

class CategoryStore(models.Model):
    menu_id = models.ForeignKey(MenuStore, on_delete=models.DO_NOTHING)
    category = models.CharField(max_length = 40)

class ItemStore(models.Model):
    eatery_id = models.ForeignKey(EateryStore, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=40)
    description = models.CharField(max_length = 200, blank=True)
    base_price = models.FloatField(null = True, blank=True)

class SubItemStore(models.Model):
    item_id = models.ForeignKey(ItemStore, on_delete=models.DO_NOTHING)
    additional_price = models.FloatField(null = True, blank=True)
    total_price = models.FloatField(null = True, blank=True)
    name = models.CharField(max_length=40)
    item_subsection = models.CharField(max_length=40)

class CategoryItemAssociation(models.Model):
    item_id = models.ForeignKey(ItemStore, on_delete=models.DO_NOTHING)
    category_id = models.ForeignKey(CategoryStore, on_delete=models.DO_NOTHING)


class EventDescription(models.TextChoices):
    BREAKFAST = 'BRKFST'
    BRUNCH = 'BRNCH'
    LUNCH = 'LNCH'
    DINNER = 'DNNR'
    GENERAL = 'GNRL'

class EventSchedule(models.Model):
    eatery_id: models.ForeignKey(EateryStore, on_delete=models.DO_NOTHING)

class DayOfWeekEventSchedule(EventSchedule):
     
    class DayOfTheWeek(models.TextChoices):
        MONDAY = 'MON'
        TUESDAY = 'TUE'
        WEDNESDAY = 'WED'
        THURSDAY = 'THU'
        FRIDAY = 'FRI'
        SATURDAY = 'SAT'
        SUNDAY = 'SUN'

    event_description: models.CharField(choices=EventDescription.choices, max_length = 10)
    menu: models.ForeignKey(MenuStore, on_delete=models.DO_NOTHING)
    day_of_week = models.CharField(choices = DayOfTheWeek.choices, max_length=3)
    start = models.TimeField()
    end = models.TimeField()

class DateEventSchedule(EventSchedule):
    event_description: models.CharField(choices=EventDescription.choices, max_length = 10)
    menu: models.ForeignKey(MenuStore, on_delete=models.DO_NOTHING)
    canonical_date = models.DateField()
    start_timestamp = models.DateTimeField()
    end_timestamp = models.DateTimeField()

class ClosedEventSchedule(EventSchedule):
    event_description: models.CharField(choices=EventDescription.choices, max_length = 10)
    canonical_date = models.DateField()


