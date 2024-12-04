from rest_framework import serializers
from user.models import User
from fcm_django.models import FCMDevice


class FCMDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FCMDevice
        fields = ["id", "registration_id", "type", "device_id", "created_at"]


class UserSerializer(serializers.ModelSerializer):
    favorite_items = serializers.ListField(
        child=serializers.CharField(max_length=100), required=False
    )
    fcm_devices = FCMDeviceSerializer(many=True, read_only=True, source="fcmdevice_set")

    class Meta:
        model = User
        fields = [
            "id",
            "given_name",
            "family_name",
            "netid",
            "google_id",
            "favorite_eateries",
            "favorite_items",
            "fcm_devices",
        ]
