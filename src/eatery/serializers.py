from rest_framework import serializers
import eatery.models as models
from event.serializers import EventSerializer


class EaterySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    menu_summary = serializers.CharField(allow_null=True)
    image_url = serializers.URLField(allow_null=True)
    location = serializers.CharField(allow_null=True)
    campus_area = serializers.CharField(allow_null=True)
    online_order_url = serializers.URLField(allow_null=True)
    latitude = serializers.FloatField(allow_null=True)
    longitude = serializers.FloatField(allow_null=True)
    payment_accepts_meal_swipes = serializers.BooleanField(allow_null=True)
    payment_accepts_brbs = serializers.BooleanField(allow_null=True)
    payment_accepts_cash = serializers.BooleanField(allow_null=True)

    events = EventSerializer(many=True, read_only=True)

    class Meta:
        model = models.Eatery
        fields = ['id', 'name', 'menu_summary', 'image_url', 'location', 'campus_area', 'online_order_url', 'latitude', 'longitude', 'payment_accepts_meal_swipes', 'payment_accepts_brbs', 'payment_accepts_cash', 'events']
