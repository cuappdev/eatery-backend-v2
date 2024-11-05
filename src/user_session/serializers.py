from rest_framework import serializers
from user_session.models import UserSession

class UserSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSession
        fields = ['id', 'user', 'session_token', 'created_at']