from django.db import models
from eatery.models import Eatery

class Item(models.Model):
    id = models.AutoField(primary_key=True)
    eatery = models.ForeignKey(Eatery, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=40, default = "Item")
    #description = models.CharField(max_length=200, blank=True)
    base_price = models.FloatField(null=True, blank=True)
    
"""    class Meta:
        abstract = True"""