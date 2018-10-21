from rest_framework import serializers
from events.models import Event

class EventSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Event
        fields = (
            'event_name',
            'id',
            'event_description',
            'creation_date',
            'event_date',
            'event_location',
            'event_participants'
        )

