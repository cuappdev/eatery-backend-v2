from rest_framework import serializers
from user.models import User


class UserSerializer(serializers.ModelSerializer):

    favorite_items = serializers.ListField(
        child=serializers.CharField(max_length=100), required=False
    )

    class Meta:
        model = User
        fields = [
            "id",
            "device_id",
            "fcm_token",
            "favorite_eateries",
            "favorite_items",
            "brb_balance",
            "city_bucks_balance",
            "laundry_balance",
            "brb_account_name",
            "city_bucks_account_name",
            "laundry_account_name",
        ]
