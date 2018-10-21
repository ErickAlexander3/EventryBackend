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
            'event_location',
            'event_participants',
            'event_start_time',
            'event_type',
            'event_end_time',
            'event_price',
            'event_qrenabled',
            'event_pic',
        )

