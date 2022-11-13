from rest_framework import serializers
from category.models import Category


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only = True)
    menu = serializers.IntegerField()
    category = serializers.CharField(allow_null = True)

    class Meta: 
        model = Category
        fields = "__all__"