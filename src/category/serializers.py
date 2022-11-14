from rest_framework import serializers
from category.models import Category
from item.serializers import ItemSerializer


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only = True)
    #menu = serializers.IntegerField()
    category = serializers.CharField(allow_null = True)

    items = ItemSerializer(many=True, read_only=True)

    class Meta: 
        model = Category
        fields = ['id', 'category', 'items']