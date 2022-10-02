from rest_framework import serializers

import api.models as models

class MenuStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MenuStore
        fields = "__all__"


class ItemStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ItemStore
        fields = "__all__"


class SubItemStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SubItemStore
        fields = "__all__"


class CategoryStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CategoryStore
        fields = "__all__"


class CategoryItemAssociationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CategoryItemAssociation
        fields = "__all__"

