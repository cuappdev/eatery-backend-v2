from rest_framework import serializers
from category.models import Category
from item.serializers import ItemSerializer, ItemSerializerOptimized


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


class CategorySerializerOptimized(serializers.ModelSerializer):
    items = ItemSerializerOptimized(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ["id", "category", "items"]
