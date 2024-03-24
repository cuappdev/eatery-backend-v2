from django.db import models


# Create your models here.
class User(models.Model):
    netid = models.CharField(max_length=40, default="User")
    token = models.CharField(max_length=40, default="User")
    name = models.CharField(max_length=40, default="User")
    favorite_items = models.ManyToManyField(
        "item.Item", related_name="favorited_by", blank=True
    )
    favorite_eateries = models.ManyToManyField(
        "eatery.Eatery", related_name="favorited_by", blank=True
    )
    is_admin = models.BooleanField(default=False)
    last_active = models.DateTimeField(auto_now=True)
