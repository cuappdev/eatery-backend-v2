from django.db import models
from event.models import Event

class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    event = models.ForeignKey(Event, related_name="menus", on_delete = models.DO_NOTHING)

    """class Meta:
        unique_together = ("eatery", "name")"""