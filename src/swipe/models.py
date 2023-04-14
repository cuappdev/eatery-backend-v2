from django.db import models
from eatery.models import Eatery
# Create your models here.
class Swipe(models.Model):

    id = models.AutoField(primary_key=True)
    eatery = models.ForeignKey(Eatery, related_name = "swipe_data", on_delete=models.DO_NOTHING)
    end_time = models.IntegerField()
    session_type = models.CharField(max_length=40)
    start_time = models.IntegerField()
    swipe_density = models.FloatField()
    wait_time_high = models.IntegerField()
    wait_time_low = models.IntegerField()
