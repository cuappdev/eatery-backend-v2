from rest_framework import serializers

import eatery.models as models


class EaterySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Eatery
        fields = "__all__"
