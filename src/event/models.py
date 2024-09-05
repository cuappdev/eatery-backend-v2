from django.db import models
from django.db import connection

from eatery.models import Eatery


class EventDescription(models.TextChoices):
    BREAKFAST = "Breakfast"
    BRUNCH = "Brunch"
    LUNCH = "Lunch"
    DINNER = "Dinner"
    GENERAL = "General"
    CAFE = "Cafe"
    PANTS = "Pants"


class Event(models.Model):
    eatery = models.ForeignKey(
        Eatery, related_name="events", on_delete=models.DO_NOTHING
    )
    event_description = models.TextField(
        choices=EventDescription.choices,
        default=EventDescription.GENERAL,
        blank=True,
        null=True,
    )
    start = models.IntegerField(default=0)
    end = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.eatery.name}: {self.event_description} from {self.start} to {self.end}"

    @classmethod
    def truncate(cls):
        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE {} CASCADE".format(cls._meta.db_table))
