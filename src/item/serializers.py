from rest_framework import serializers
from item.models import Item

class ItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only = True)
    eatery = serializers.IntegerField()
    name = serializers.CharField(default = "Item")


    class Meta:
        model = Item
        fields = "__all__"