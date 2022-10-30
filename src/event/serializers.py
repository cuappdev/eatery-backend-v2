from rest_framework import serializers
from models import Event, Menu, Category, Item, SubItem, CategoryItemAssociation

class EventSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta: 
        model = Event 
        fields = ['id', 'eatery', 'event_description', 'start', 'end']

class MenuSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    categories = serializers.StringRelatedField(allow_null=True)

    class Meta:
        model = Menu
        fields = ['id', 'categories']


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"


class SubItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubItem
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CategoryItemAssociationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryItemAssociation
        fields = "__all__"


