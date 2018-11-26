
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
    number_of_registered = serializers.ReadOnlyField(source='registered_users.count')
    number_of_attending = serializers.ReadOnlyField(source='attending_users.count')
    is_hosting = serializers.SerializerMethodField()
    is_registered = serializers.SerializerMethodField()
    is_attending = serializers.SerializerMethodField()
    is_favourite = serializers.SerializerMethodField()

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
            'number_of_registered',
            'number_of_attending',
            'event_max_capacity',
            'event_type',
            'event_start_time',
            'event_end_time',
            'event_price',
            'event_media',
            'room_id',
            'distance',
            'rank',
            'is_hosting',
            'is_attending',
            'is_registered',
            'is_favourite'
        )

    def get_is_hosting(self, obj):
        return self.context["request"].user.id == obj.host.id

    def get_is_registered(self, obj):
        return obj.registered_users.filter(id=self.context["request"].user.id).exists()

    def get_is_attending(self, obj):
        return obj.attending_users.filter(id=self.context["request"].user.id).exists()

    def get_is_favourite(self, obj):
        return obj.favourited_users.filter(id=self.context["request"].user.id).exists()

    '''
    def create(self, validated_data):
        #create event
        event = Event.objects.create(**validated_data)

        #if images added, do the bindings
        if "event_media" in self.context["request"].data:
            for image_data in self.context["request"].data.getlist("event_media"):
                eventImage = EventImage.objects.create(event=event)
                eventImage.image.save(image_data.name, image_data)
        return event
    '''