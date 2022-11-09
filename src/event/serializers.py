from rest_framework import serializers
from event.models import Event


class EventSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, read_only = True)
    event_description = serializers.CharField(allow_null=True)
    start = serializers.DateTimeField() 
    end = serializers.DateTimeField()
        
    def create(self, validated_data):
        return Event.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.event_description = validated_data.get('event_description', instance.event_description)
        instance.start = validated_data.get('start', instance.start)
        instance.end = validated_data.get('end', instance.end)
        instance.save()
        return instance
    def get_validation_exclusions(self):
        exclusions = super(EventSerializer, self).get_validation_exclusions()
        return exclusions + ['id']

    class Meta: 
        model = Event 
        fields = ['id', 'eatery', 'event_description', 'start', 'end']