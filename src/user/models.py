from django.db import models
from fcm_django.models import FCMDevice


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
        return f"{self.netid}"


class UserFCMDevice(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="fcm_devices",
        null=True,
        blank=True,
    )
    registration_id = models.CharField(
        max_length=255, default="default_registration_id"
    )
    device_id = models.CharField(
        max_length=255, unique=True, default="default_device_id"
    )
    type = models.CharField(
        max_length=10, default="unknown"
    )  # e.g., 'ios', 'android', 'web'

    def __str__(self):
        return f"FCM Device {self.device_id} ({self.type})"
