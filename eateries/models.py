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
    description = models.CharField(max_length = 100)
    start_timestamp = models.DateTimeField()
    end_timestamp = models.DateTimeField()

class MenuItemStore(models.Model):
    eatery_id = models.ForeignKey(EateryStore, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=40)
    description = models.CharField(max_length = 100, blank=True)
    base_price = models.FloatField(null = True, blank=True)

class MenuSubItemStore(models.Model):
    item_id = models.ForeignKey(MenuItemStore, on_delete=models.DO_NOTHING)
    additional_price = models.FloatField(null = True, blank=True)
    total_price = models.FloatField(null = True, blank=True)
    name = models.CharField(max_length=40)
    item_subsection = models.CharField(max_length=40)


class MenuStore(models.Model):
    eatery_id = models.ForeignKey(EateryStore, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length = 40)

class ForSale(models.Model):
    item_id = models.ForeignKey(MenuItemStore, on_delete=models.DO_NOTHING)
    menu_id = models.ForeignKey(MenuStore, on_delete=models.DO_NOTHING)
    category = models.CharField(max_length=40)

class EventDescription(models.TextChoices):
    BREAKFAST = 'BRKFST'
    LUNCH = 'LNCH'
    DINNER = 'DNNR'
    GENERAL = 'GNRL'

class RepeatingEventSchedule(models.Model):
    class DayOfTheWeek(models.TextChoices):
        MONDAY = 'MON'
        TUESDAY = 'TUE'
        WEDNESDAY = 'WED'
        THURSDAY = 'THU'
        FRIDAY = 'FRI'
        SATURDAY = 'SAT'
        SUNDAY = 'SUN'
    
    eatery_id = models.ForeignKey(EateryStore, on_delete=models.DO_NOTHING)
    menu = models.ForeignKey(MenuStore, on_delete=models.DO_NOTHING)
    day_of_week = models.CharField(choices = DayOfTheWeek.choices, max_length=3)
    event_description = models.CharField(choices=EventDescription.choices, max_length = 10)
    start = models.TimeField()
    end = models.TimeField()

class EventChangeLog(models.Model):
    class Meta:
        indexes = [
            models.Index(fields = ['eatery_id', 'canonical_date']), 
            models.Index(fields = ['created_at'])
        ] 
    class ChangeLogType(models.TextChoices):
        INSERT = 'INS'
        DELETE = 'DEL'
    
    eatery_id = models.ForeignKey(EateryStore, on_delete = models.DO_NOTHING)
    menu = models.ForeignKey(MenuStore, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(default=datetime.now)
    type = models.CharField(choices=ChangeLogType.choices, max_length=3)
    event_description = models.CharField(choices=EventDescription.choices, max_length= 10)
    canonical_date = models.DateField()
    start = models.DateTimeField()
    end = models.DateTimeField()



