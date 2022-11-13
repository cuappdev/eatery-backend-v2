from django.db import models 

from eatery.models import Eatery

class EventDescription(models.TextChoices):
    BREAKFAST = "Breakfast"
    BRUNCH = "Brunch"
    LUNCH = "Lunch"
    DINNER = "Dinner"
    GENERAL = "General"
    CAFE = "Cafe"

class Event(models.Model): 
    id = models.AutoField(primary_key=True)
    eatery = models.ForeignKey(Eatery, on_delete=models.DO_NOTHING)
    event_description = models.CharField(
        choices=EventDescription.choices, max_length=10, default = EventDescription.GENERAL, blank=True, null = True)
    start = models.DateTimeField(auto_now_add=True) #combine canonical_date w/ start/end timestamp
    end = models.DateTimeField(auto_now_add=True)
