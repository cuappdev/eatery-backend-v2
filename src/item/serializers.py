from rest_framework import serializers
from item.models import Item

class ItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only = True)
    name = serializers.CharField(default = "Item")

    def create(self, validated_data):
        return Item.objects.get_or_create(**validated_data)

    class Meta:
        model = Item
        fields = ['id', 'name']