from django.db import models
from event.models import Event

class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    #eatery = models.ForeignKey(Eatery, on_delete=models.DO_NOTHING)
    event = models.ForeignKey(Event, on_delete = models.DO_NOTHING)
    #name = models.CharField(max_length=40)

    """class Meta:
        unique_together = ("eatery", "name")"""