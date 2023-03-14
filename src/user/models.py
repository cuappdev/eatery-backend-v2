from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
      netid = models.TextField(unique=True)
      favorite_items = models.ManyToManyField('item.Item', related_name='users', blank=True)

def __str__(self):
      return self.netid