from rest_framework import serializers

import eatery.models as models


class EateryStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EateryStore
        fields = "__all__"