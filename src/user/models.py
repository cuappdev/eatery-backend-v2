from django.db import models
from django.contrib.postgres.fields import ArrayField


class User(models.Model):
    device_id = models.CharField(max_length=100, blank=True)
    fcm_token = models.CharField(max_length=100, blank=True)
    favorite_items = ArrayField(
        models.CharField(max_length=100), blank=True, default=list
    )
    favorite_eateries = models.ManyToManyField(
        "eatery.Eatery", related_name="favorited_by", blank=True
    )
    brb_account_name = models.CharField(max_length=255, blank=True)
    city_bucks_account_name = models.CharField(max_length=255, blank=True)
    laundry_account_name = models.CharField(max_length=255, blank=True)

    brb_balance = models.FloatField(default=0)
    city_bucks_balance = models.FloatField(default=0)
    laundry_balance = models.FloatField(default=0)

    def __str__(self):
        return f"{self.netid}"
