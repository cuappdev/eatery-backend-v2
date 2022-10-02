from rest_framework import serializers

import AlertModel 

class AlertStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertModel.AlertStore
        fields = "__all__"
