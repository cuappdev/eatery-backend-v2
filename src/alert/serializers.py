from rest_framework import serializers

from alert.models import Alert

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ['id', 'description', 'start_timestamp', 'end_timestamp']
