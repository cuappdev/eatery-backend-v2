from rest_framework import serializers
from category.models import Category
from item.serializers import ItemSerializer, ItemReadSerializer


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    category = serializers.CharField(allow_null=True)
    items = ItemSerializer(many=True, read_only=True)

    def create(self, validated_data):
        category, _ = Category.objects.get_or_create(**validated_data)
        return category

    class Meta:
        model = Category
        fields = ["id", "category", "event", "items"]

class CategoryReadSerializer(serializers.ModelSerializer):
    items = ItemReadSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["category", "items"]
