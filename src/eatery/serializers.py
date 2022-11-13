from rest_framework import serializers
import eatery.models as models


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

    class Meta:
        model = models.Eatery
        fields = "__all__"
