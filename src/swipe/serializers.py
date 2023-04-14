from rest_framework import serializers
from swipe.models import Swipe


class SwipeSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField()
    end_time = serializers.IntegerField()
    session_type = serializers.CharField(max_length=40)
    start_time = serializers.IntegerField()
    swipe_density = serializers.FloatField()
    wait_time_high = serializers.IntegerField()
    wait_time_low = serializers.IntegerField()