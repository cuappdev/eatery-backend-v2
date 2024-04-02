from rest_framework import serializers
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "netid",
            "token",
            "name",
            "favorite_items",
            "favorite_eateries",
            "is_admin",
            "last_active",
        ]
