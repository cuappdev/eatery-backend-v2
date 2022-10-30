from wsgiref import validate
from rest_framework import serializers

from models import Alert 

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = "__all__"

    def create(self, validated_data):
        """
        Create and return a new Alert.
        """
        return Alert.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update an existing Alert.
        """
        instance.description = validated_data.get('description', instance.description)
        instance.start_timestamp = validated_data.get('start_timestamp',instance.start_timestamp)
        instance.end_timestamp = validated_data.get('end_timestamp', instance.end_timestamp)

        instance.save()
        return instance 

class AlertSubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = ['id', 'description', 'start_timestamp', 'end_timestamp']
