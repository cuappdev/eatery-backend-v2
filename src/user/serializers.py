from rest_framework import serializers
from user.models import User
from device_token.models import DeviceToken


class UserSerializer(serializers.ModelSerializer):
    favorite_items = serializers.ListField(
        child=serializers.CharField(max_length=100), required=False
    )

    device_tokens = serializers.PrimaryKeyRelatedField(
        many=True, queryset=DeviceToken.objects.all(), required=False
    )

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
            "device_tokens",
        ]
