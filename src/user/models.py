from django.db import models
from django.contrib.postgres.fields import ArrayField


class User(models.Model):
    netid = models.CharField(max_length=10, null=True, blank=True)
    given_name = models.CharField(max_length=30, null=True, blank=True)
    family_name = models.CharField(max_length=30, null=True, blank=True)
    google_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    favorite_items = ArrayField(
        models.CharField(max_length=100), blank=True, default=list
    )
    favorite_eateries = models.ManyToManyField(
        "eatery.Eatery", related_name="favorited_by", blank=True
    )

    def __str__(self):
        return f"{self.netid}"
