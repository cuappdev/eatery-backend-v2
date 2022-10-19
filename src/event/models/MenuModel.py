from django.db import models
from eatery.models import EateryStore


class MenuStore(models.Model):
    id = models.IntegerField(primary_key=True)
    eatery = models.ForeignKey(EateryStore, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=40)

    class Meta:
        unique_together = ("eatery", "name")


class CategoryStore(models.Model):
    id = models.IntegerField(primary_key=True)
    menu = models.ForeignKey(MenuStore, on_delete=models.DO_NOTHING)
    category = models.CharField(max_length=40)

    class Meta:
        unique_together = ("menu", "category")


class ItemStore(models.Model):
    id = models.IntegerField(primary_key=True)
    eatery = models.ForeignKey(EateryStore, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=200, blank=True)
    base_price = models.FloatField(null=True, blank=True)


class SubItemStore(models.Model):
    id = models.IntegerField(primary_key=True)
    item = models.ForeignKey(ItemStore, on_delete=models.DO_NOTHING)
    additional_price = models.FloatField(null=True, blank=True)
    total_price = models.FloatField(null=True, blank=True)
    name = models.CharField(max_length=40)
    item_subsection = models.CharField(max_length=40)


class CategoryItemAssociation(models.Model):
    id = models.IntegerField(primary_key=True)
    item = models.ForeignKey(ItemStore, on_delete=models.DO_NOTHING)
    category = models.ForeignKey(CategoryStore, on_delete=models.DO_NOTHING)
