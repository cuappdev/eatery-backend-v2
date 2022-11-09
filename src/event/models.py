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
        choices=EventDescription.choices, max_length=10, default = EventDescription.GENERAL)
    start = models.DateTimeField(auto_now_add=True) #combine canonical_date w/ start/end timestamp
    end = models.DateTimeField(auto_now_add=True)



class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    #eatery = models.ForeignKey(Eatery, on_delete=models.DO_NOTHING)
    event = models.ForeignKey(Event, on_delete = models.DO_NOTHING)
    #name = models.CharField(max_length=40)

    """class Meta:
        unique_together = ("eatery", "name")"""


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    menu = models.ForeignKey(Menu, on_delete=models.DO_NOTHING)
    category = models.CharField(max_length=40, default="General")

"""    class Meta:
        abstract = True
        unique_together = ("menu", "category")"""


class Item(models.Model):
    id = models.AutoField(primary_key=True)
    eatery = models.ForeignKey(Eatery, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=40, default = "Item")
    #description = models.CharField(max_length=200, blank=True)
    base_price = models.FloatField(null=True, blank=True)
    
"""    class Meta:
        abstract = True"""


class SubItem(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING)
    additional_price = models.FloatField(null=True, blank=True)
    total_price = models.FloatField(null=True, blank=True)
    name = models.CharField(max_length=40, default = "SubItem")
    item_subsection = models.CharField(max_length=40)

"""    class Meta:
        abstract = True"""

class CategoryItemAssociation(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
