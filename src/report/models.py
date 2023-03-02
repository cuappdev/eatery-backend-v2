from django.db import models
from eatery.models import Eatery


class Report(models.Model):
    eatery = models.ForeignKey(Eatery, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

def __str__(self):
      return self.content