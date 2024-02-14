from rest_framework import serializers
from eatery.models import Eatery
from event.models import Event
from event.serializers import EventSerializer, EventSerializerSimple, EventReadSerializer
from django.utils import timezone
from datetime import date, timedelta
from time import mktime

class EaterySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    menu_summary = serializers.CharField(allow_null=True,default="Cornell Eatery")
    image_url = serializers.URLField(allow_null=True,default="https://images-prod.healthline.com/hlcmsresource/images/AN_images/health-benefits-of-apples-1296x728-feature.jpg")
    location = serializers.CharField(allow_null=True)
    campus_area = serializers.CharField(allow_null=True)
    online_order_url = serializers.URLField(allow_null=True)
    latitude = serializers.FloatField(allow_null=True)
    longitude = serializers.FloatField(allow_null=True)
    payment_accepts_meal_swipes = serializers.BooleanField(allow_null=True)
    payment_accepts_brbs = serializers.BooleanField(allow_null=True)
    payment_accepts_cash = serializers.BooleanField(allow_null=True)

    events = EventSerializer(many=True, read_only=True)

    def create(self, validated_data):
        eatery, _ = Eatery.objects.get_or_create(**validated_data)
        return eatery
    
    class Meta:
        model = Eatery
        fields = ['id', 'name', 'menu_summary', 'image_url', 'location', 'campus_area', 'online_order_url', 'latitude', 'longitude', 'payment_accepts_meal_swipes', 'payment_accepts_brbs', 'payment_accepts_cash', 'events']
    
class EateryReadSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    menu_summary = serializers.CharField(allow_null=True,default="Cornell Eatery")
    image_url = serializers.URLField(allow_null=True,default="https://images-prod.healthline.com/hlcmsresource/images/AN_images/health-benefits-of-apples-1296x728-feature.jpg")
    location = serializers.CharField(allow_null=True)
    campus_area = serializers.CharField(allow_null=True)
    online_order_url = serializers.URLField(allow_null=True)
    latitude = serializers.FloatField(allow_null=True)
    longitude = serializers.FloatField(allow_null=True)
    payment_accepts_meal_swipes = serializers.BooleanField(allow_null=True)
    payment_accepts_brbs = serializers.BooleanField(allow_null=True)
    payment_accepts_cash = serializers.BooleanField(allow_null=True)
    events = EventReadSerializer(many=True, read_only=True)

    class Meta:
        model = Eatery
        fields = ['id', 'name', 'menu_summary', 'image_url', 'location', 'campus_area', 'online_order_url', 'latitude', 'longitude', 'payment_accepts_meal_swipes', 'payment_accepts_brbs', 'payment_accepts_cash', 'events']


class EaterySerializerSimple(serializers.ModelSerializer):
    menu_summary = serializers.CharField(allow_null=True,default="Cornell Eatery")
    image_url = serializers.URLField(allow_null=True,default="https://images-prod.healthline.com/hlcmsresource/images/AN_images/health-benefits-of-apples-1296x728-feature.jpg")
    events = EventSerializerSimple(many=True, read_only=True)

    class Meta:
        model = Eatery
        fields = ['id', 'name', 'menu_summary', 'image_url', 'location', 'campus_area', 'online_order_url', 'latitude', 'longitude', 'payment_accepts_meal_swipes', 'payment_accepts_brbs', 'payment_accepts_cash', 'events']

class EaterySerializerByDay(serializers.ModelSerializer):
    menu_summary = serializers.CharField(allow_null=True,default="Cornell Eatery")
    image_url = serializers.URLField(allow_null=True,default="https://images-prod.healthline.com/hlcmsresource/images/AN_images/health-benefits-of-apples-1296x728-feature.jpg")
    events = serializers.SerializerMethodField()

    def get_events(self, obj):
        day = self.context.get("day")
        today = timezone.now().date()
        today = today + timedelta(days=day)
        end_today = today + timedelta(days=1)
        today_unix = mktime(today.timetuple())
        end_today_unix = mktime(end_today.timetuple())
        events = Event.objects.filter(eatery=obj.id, start__gte=today_unix, start__lte=end_today_unix)
        serializer = EventReadSerializer(instance=events, many=True)
        return serializer.data

    class Meta:
        model = Eatery
        fields = ['id', 'name', 'menu_summary', 'image_url', 'location', 'campus_area', 'online_order_url', 'latitude', 'longitude', 'payment_accepts_meal_swipes', 'payment_accepts_brbs', 'payment_accepts_cash', 'events']

