from rest_framework import serializers
from event.models import Category

class CategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only = True)
    menu = serializers.IntegerField()
    category = serializers.CharField(allow_null = True)

    def get_validation_exclusions(self):
        exclusions = super(CategorySerializer, self).get_validation_exclusions()
        return exclusions + ['id', 'category']

    class Meta: 
        model = Category
        fields = "__all__"