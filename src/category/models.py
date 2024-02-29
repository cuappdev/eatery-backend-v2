from django.db import models
from eatery.models import Eatery
from event.models import Event


class Category(models.Model):
    event = models.ForeignKey(Event, related_name="menu", on_delete=models.DO_NOTHING)
    category = models.CharField(max_length=40, default="General")
