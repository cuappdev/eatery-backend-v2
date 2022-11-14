from rest_framework import serializers
from menu.models import Menu
from category.serializers import CategorySerializer

class MenuSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only = True)
    
    categories = CategorySerializer(many=True, read_only=True)
    #event = serializers.IntegerField(allow_null = True)
    #categories = serializers.StringRelatedField(allow_null=True)

    def create(self, validated_data):
        return Menu.objects.create(**validated_data)

    class Meta:
        model = Menu
        fields = ['id', 'event', 'categories']