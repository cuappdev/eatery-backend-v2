from django.db import models
from event.models import Event


class Category(models.Model):
    event = models.ForeignKey(Event, related_name="menu", on_delete=models.DO_NOTHING)
    category = models.CharField(max_length=40, default="General")
    
    def __str__(self):
        return self.category
