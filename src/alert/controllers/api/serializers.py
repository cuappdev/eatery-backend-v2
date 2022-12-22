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

class RepeatingEventScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RepeatingEventSchedule
        fields = "__all__"


class ScheduleExceptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ScheduleException
        fields = "__all__"


