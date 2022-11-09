from rest_framework import serializers
from event.models import Item

class ItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    eatery = serializers.IntegerField()
    name = serializers.CharField(default = "Item")

    class Meta:
        model = Item
        fields = "__all__"