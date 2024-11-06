from rest_framework import serializers
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "netid",
            "is_admin",
            "favorite_eateries",
            "favorite_items",
            "fcm_devices",
        ]
