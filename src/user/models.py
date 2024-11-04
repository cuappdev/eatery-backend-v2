from django.db import models


class User(models.Model):
    netid = models.CharField(max_length=10, null=True, blank=True)
    name = models.CharField(max_length=40, default="User")
    favorite_items = models.ManyToManyField(
        "item.Item", related_name="favorited_by", blank=True
    )
    favorite_eateries = models.ManyToManyField(
        "eatery.Eatery", related_name="favorited_by", blank=True
    )
    is_admin = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.netid}'
        