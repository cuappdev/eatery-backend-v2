from django.db import models
from django.db import connection
from eatery.util.constants import DEFAULT_IMAGE_URL


class Eatery(models.Model):
    class CampusArea(models.TextChoices):
        WEST = "West"
        NORTH = "North"
        CENTRAL = "Central"
        COLLEGETOWN = "Collegetown"
        NONE = ""

    name = models.CharField(max_length=40)
    menu_summary = models.TextField(blank=True, null=True, default="")
    image_url = models.URLField(blank=True, default=DEFAULT_IMAGE_URL)
    location = models.TextField(blank=True)
    campus_area = models.CharField(
        max_length=15, choices=CampusArea.choices, default=CampusArea.NONE, blank=True
    )
    online_order_url = models.URLField(null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    payment_accepts_meal_swipes = models.BooleanField(null=True, blank=True)
    payment_accepts_brbs = models.BooleanField(null=True, blank=True)
    payment_accepts_cash = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return self.name
