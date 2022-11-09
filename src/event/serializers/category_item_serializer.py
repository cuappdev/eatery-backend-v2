from rest_framework import serializers
from event.models import CategoryItemAssociation

class CategoryItemAssociationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryItemAssociation
        fields = "__all__"