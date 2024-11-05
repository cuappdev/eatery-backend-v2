from django.db import models


class User(models.Model):
    netid = models.CharField(max_length=10, null=True, blank=True)
    given_name = models.CharField(max_length=30, null=True, blank=True)
    family_name = models.CharField(max_length=30, null=True, blank=True)
    google_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    favorite_items = models.ManyToManyField(
        "item.Item", related_name="favorited_by", blank=True
    )
    favorite_eateries = models.ManyToManyField(
        "eatery.Eatery", related_name="favorited_by", blank=True
    )
    
    def __str__(self):
        return f'{self.netid}'
        