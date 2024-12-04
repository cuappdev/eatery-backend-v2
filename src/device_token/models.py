from django.db import models
from user.models import User


class DeviceToken(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, related_name="device_tokens", on_delete=models.CASCADE
    )
    device_token = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.user.netid} - {self.device_token}"
