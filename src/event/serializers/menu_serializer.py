from rest_framework import serializers
from event.models import Menu

class MenuSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    categories = serializers.StringRelatedField(allow_null=True)

    def create(self, validated_data):
        return Menu.objects.create(**validated_data)
    

    class Meta:
        model = Menu
        fields = ['id', 'categories']