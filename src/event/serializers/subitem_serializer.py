from rest_framework import serializers
from event.models import SubItem

class SubItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = SubItem
        fields = "__all__"