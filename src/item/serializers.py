from rest_framework import serializers
from item.models import Item

class ItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only = True)
    name = serializers.CharField(default = "Item")

    def create(self, validated_data):
        item, _ =  Item.objects.get_or_create(**validated_data)
        return item

    class Meta:
        model = Item
        fields = ['id', 'category', 'name']

class ItemSerializerOptimized(serializers.ModelSerializer):
    name = serializers.CharField(default = "Item")

    class Meta:
        model = Item
        fields = ['name']