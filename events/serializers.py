from rest_framework import serializers
from events.models import Event
from drf_extra_fields.geo_fields import PointField

class EventSerializer(serializers.HyperlinkedModelSerializer):
    event_point_location = PointField(required=False)

    class Meta:
        model = Event
        fields = (
            'event_name',
            'id',
            'event_description',
            'creation_date',
            'event_point_location',
            'event_address',
            'event_participants',
            'event_start_time',
            #'event_type',
            'event_end_time',
            'event_price',
            'event_qrenabled',
            'event_pic',
        )

