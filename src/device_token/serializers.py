from rest_framework import serializers
from device_token.models import DeviceToken

class DeviceTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceToken
        fields = ['id', 'user', 'device_token']