from django.db import models

# Create your models here.
class Swipe(models.model):

    id = models.AutoField(primary_key=True)
    end_time = models.IntegerField()
    session_type = models.CharField(max_length=40)
    start_time = models.IntegerField()
    swipe_density = models.FloatField()
    wait_time_high = models.IntegerField()
    wait_time_low = models.IntegerField()
