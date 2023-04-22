from rest_framework import serializers
from swipe.models import WaitTime

class WaitSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    canonical_date = serializers.IntegerField()
    wait_time_high = serializers.IntegerField()
    wait_time_expected= serializers.IntegerField()
    wait_time_low = serializers.IntegerField()
    day = serializers.CharField(
        allow_null=True, allow_blank=True, default=None
    )
    hour = serializers.IntegerFIeld()

    def create(self, validated_data):
        wait_time, _ = WaitTime.objects.get_or_create(**validated_data)
        return wait_time
    class Meta:
        model = WaitTime
        fields = ["id", "canonical_date", "eatery", "day", "hour", "wait_time_high", "wait_time_expected", "wait_time_low"]
        