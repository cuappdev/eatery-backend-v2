from django.db import models
from datetime import datetime
class EateryStore(models.Model):
    class CampusArea(models.TextChoices):
        WEST = 'West'
        NORTH = 'North'
        CENTRAL = 'Central'
        COLLEGETOWN = 'Collegetown'
        NONE = ''

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40, blank=True)
    menu_summary = models.CharField(max_length = 60, blank=True)
    image_url = models.URLField(blank=True)
    location = models.CharField(max_length=30, blank=True)
    campus_area = models.CharField(max_length=15, choices=CampusArea.choices, default=CampusArea.NONE, blank=True)
    online_order_url = models.URLField(blank=True)
    latitude = models.FloatField(null = True, blank=True)
    longitude = models.FloatField(null = True, blank=True)
    payment_accepts_meal_swipes = models.BooleanField(null = True, blank=True)
    payment_accepts_brbs = models.BooleanField(null = True, blank=True)
    payment_accepts_cash = models.BooleanField(null = True, blank=True)

class AlertStore(models.Model):
    id = models.IntegerField(primary_key=True)
    eatery = models.ForeignKey(EateryStore, on_delete=models.DO_NOTHING)
    description = models.CharField(max_length = 250)
    start_timestamp = models.IntegerField()
    end_timestamp = models.IntegerField()

class MenuStore(models.Model):
    id = models.IntegerField(primary_key=True)
    eatery = models.ForeignKey(EateryStore, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length = 40)

    class Meta:
        unique_together = ('eatery', 'name')

class CategoryStore(models.Model):
    id = models.IntegerField(primary_key=True)
    menu = models.ForeignKey(MenuStore, on_delete=models.DO_NOTHING)
    category = models.CharField(max_length = 40)

    class Meta:
        unique_together = ('menu', 'category')

class ItemStore(models.Model):
    id = models.IntegerField(primary_key=True)
    eatery = models.ForeignKey(EateryStore, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=40)
    description = models.CharField(max_length = 200, blank=True)
    base_price = models.FloatField(null = True, blank=True)

class SubItemStore(models.Model):
    id = models.IntegerField(primary_key=True)
    item = models.ForeignKey(ItemStore, on_delete=models.DO_NOTHING)
    additional_price = models.FloatField(null = True, blank=True)
    total_price = models.FloatField(null = True, blank=True)
    name = models.CharField(max_length=40)
    item_subsection = models.CharField(max_length=40)

class CategoryItemAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    item = models.ForeignKey(ItemStore, on_delete=models.DO_NOTHING)
    category = models.ForeignKey(CategoryStore, on_delete=models.DO_NOTHING)
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


