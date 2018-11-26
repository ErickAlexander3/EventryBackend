
from rest_framework import serializers
from events.models import Event, EventImage
from drf_extra_fields.geo_fields import PointField
from rest_framework.fields import ListField

import pdb

class EventImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventImage
        fields = ('image',)

class EventSerializer(serializers.HyperlinkedModelSerializer):
    host = serializers.ReadOnlyField(source='host.username')
    event_point_location = PointField(required=False)
    event_type = ListField(required=False)
    event_media = EventImageSerializer(many=True, read_only=True) #
    event_start_time = serializers.DateTimeField(input_formats=["%Y-%m-%dT%H:%M:%S.%fZ"])
    event_end_time = serializers.DateTimeField(input_formats=["%Y-%m-%dT%H:%M:%S.%fZ"])
    room_id = serializers.ReadOnlyField()
    distance = serializers.ReadOnlyField(source='distance.km')
    rank = serializers.ReadOnlyField()

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
            'event_media',
            'room_id',
            'distance',
            'rank'
        )


    def create(self, validated_data):
        #create event
        event = Event.objects.create(**validated_data)

        #if images added, do the bindings
        if "event_media" in self.context["request"].data:
            for image_data in self.context["request"].data.getlist("event_media"):
                eventImage = EventImage.objects.create(event=event)
                eventImage.image.save(image_data.name, image_data)
        return event
