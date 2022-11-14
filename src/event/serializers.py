from rest_framework import serializers
from event.models import Event

class EventSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, read_only = True)
    event_description = serializers.CharField(allow_null=True, allow_blank = True, default=None)
    start = serializers.DateTimeField()
    end = serializers.DateTimeField()
        
    def create(self, validated_data):
        return Event.objects.create(**validated_data)

    class Meta: 
        model = Event 
        fields = ['id', 'eatery', 'event_description', 'start', 'end']