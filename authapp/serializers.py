'''
from events.models import Event
from drf_extra_fields.geo_fields import PointField
from rest_framework.fields import ListField

class UserSerializer(serializers.HyperlinkedModelSerializer):
    host = serializers.ReadOnlyField(source='host.username')
    event_point_location = PointField(required=False)
    event_type = ListField()

    class Meta:
        model = Event
        fields = (
            'host',
            'event_name',
            'id',
            'event_description',
            'creation_date',
            'event_point_location',
            'event_address',
            'event_max_capacity',
            'event_type',
            'event_start_time',
            #'event_type',
            'event_end_time',
            'event_price',
            'event_pic',
        )
'''