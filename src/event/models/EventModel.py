from django.db import models 

from event.models.MenuModel import MenuStore
from src.eatery.models import EateryStore

class EventDescription(models.TextChoices):
    BREAKFAST = "Breakfast"
    BRUNCH = "Brunch"
    LUNCH = "Lunch"
    DINNER = "Dinner"
    GENERAL = "General"


class EventStore(models.Model): 
    id = models.IntegerField(primary_key=True)
    eatery = models.ForeignKey(EateryStore, on_delete=models.DO_NOTHING)
    event_description = models.CharField(
        choices=EventDescription.choices, max_length=10
    )
    menu = models.ForeignKey(MenuStore, on_delete=models.DO_NOTHING)
    start = models.DateTimeField() #combine canonical_date w/ start/end timestamp
    end = models.DateTimeField()

    class Meta:
        abstract = True

