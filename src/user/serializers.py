from rest_framework import serializers
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'given_name', 'family_name', 'netid', 'google_id', 'favorite_eateries', 'favorite_items']
