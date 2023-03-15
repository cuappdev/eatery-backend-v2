from django.db import models 

from eatery.models import Eatery

class EventDescription(models.TextChoices):
    BREAKFAST = "Breakfast"
    BRUNCH = "Brunch"
    LUNCH = "Lunch"
    DINNER = "Dinner"
    GENERAL = "General"
    CAFE = "Cafe"
    PANTS = "Pants"

class Event(models.Model): 
    id = models.AutoField(primary_key=True)
    eatery = models.ForeignKey(Eatery, related_name = "events", on_delete=models.DO_NOTHING)
    event_description = models.TextField(
        choices=EventDescription.choices, default = EventDescription.GENERAL, blank=True, null = True)
    start = models.DateTimeField() 
    end = models.DateTimeField()
