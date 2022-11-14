from django.db import models
from eatery.models import Eatery
from menu.models import Menu

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    menu = models.ForeignKey(Menu, related_name = 'categories', on_delete=models.DO_NOTHING)
    category = models.CharField(max_length=40, default="General")

"""    class Meta:
        abstract = True
        unique_together = ("menu", "category")"""