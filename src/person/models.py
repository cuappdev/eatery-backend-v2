from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    net_id = models.TextField()
    favorite_eateries = models.ManyToManyField('eatery.Eatery', related_name='student')
    favorite_items = models.ManyToManyField('item.Item', related_name='student')
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, default=None)
    
    def __str__(self):
        return f"Student {self.net_id}"

class Chef(models.Model):
    eateries_managed = models.ManyToManyField('eatery.Eatery', related_name='chef')
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True, default=None)
    
    def __str__(self):
        return f"Chef {self.user.username}"