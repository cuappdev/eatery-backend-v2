from rest_framework import serializers
from swipe.models import WaitTime
from datetime import datetime

class DayWaitTimeSerializer(serializers.ListSerializer):

    def to_representation(self, data):
        day = WaitTime.int_to_day(datetime.now().weekday())
        data = data.filter(day=day)
        return super().to_representation(data)

class WaitTimeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, read_only=True)
    wait_time_high = serializers.IntegerField()
    wait_time_expected = serializers.IntegerField()
    wait_time_low = serializers.IntegerField()
    day = serializers.CharField(
        allow_null=True, allow_blank=True, default=None
    )
    hour = serializers.IntegerField()
    trials = serializers.IntegerField()

    def create(self, validated_data):
        wait_time, _ = WaitTime.objects.get_or_create(**validated_data)
        return wait_time
    
    class Meta:
        model = WaitTime
        fields = ["id", "eatery", "day", "hour", "wait_time_high", "wait_time_expected", "wait_time_low", "trials"]
        list_serializer_class = DayWaitTimeSerializer
    