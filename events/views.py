from events.serializers import EventSerializer
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.contrib.gis.geos import Point

from django.contrib.auth.models import User
from events.models import Event

import pdb
import json

from datetime import datetime

from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.db.models import Q

from events.models import Event, EventImage

class EventViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    """
    #queryset = Event.objects.all()
    serializer_class = EventSerializer

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)


    def get_queryset(self):
        queryset = Event.objects.all()

        if 'not_expired' in self.request.query_params:
            queryset = queryset.filter(event_end_time__gt=datetime.utcnow())

        if 'search' in self.request.query_params:
            search_vector = SearchVector('event_name', weight='A') + SearchVector('event_description', weight='A') + SearchVector('event_address', weight='B')
            search_query = SearchQuery(self.request.query_params['search'])

            queryset = queryset.annotate(rank=SearchRank(search_vector, search_query)).filter(rank__gte=0.25).order_by('-rank')

        if 'lon' in self.request.query_params and 'lat' in self.request.query_params:

            #pdb.set_trace()
            ref_location = Point(float(self.request.query_params['lon']), float(self.request.query_params['lat']))
                
            queryset = queryset.filter(
                event_point_location__distance_lt=(ref_location, D(km=500))).annotate(
                distance=Distance('event_point_location', ref_location)).order_by(
                'distance')


        return queryset

    '''
        Getters
    '''

    @action(detail=False)
    def hosting(self, request):
        hosting_events = Event.objects.filter(host__id=request.user.pk)
        serializer = self.get_serializer(hosting_events, many=True)
        return Response(serializer.data)

    @action(detail=False)
    def favourited(self, request):
        favourited_events = Event.objects.filter(favourited_users__id=request.user.pk)
        serializer = self.get_serializer(favourited_events, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def is_favourite(self, request, pk=None):
        event_to_check = self.get_object()
        is_favourite = event_to_check.favourited_users.filter(id=request.user.id).exists()
        return Response({'is_favourite': is_favourite} )

    @action(detail=False)
    def registered(self, request):
        registered_events = Event.objects.filter(registered_users__id=request.user.pk)
        serializer = self.get_serializer(registered_events, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def is_registered(self, request, pk=None):
        event_to_check = self.get_object()
        is_registered = event_to_check.registered_users.filter(id=request.user.id).exists()
        return Response({'is_registered': is_registered} )

    @action(detail=False)
    def attending(self, request):
        attending_events = Event.objects.filter(attending_users__id=request.user.pk)
        serializer = self.get_serializer(attending_events, many=True)
        return Response(serializer.data)

    '''
        Setters
    '''
    @action(detail=True, methods=['post'])
    def favourite(self, request, pk=None):
        event_to_fav = self.get_object()
        event_to_fav.favourited_users.add(request.user)
        event_to_fav.save()
        return Response({'status': 'favourited event'})

    @action(detail=True, methods=['post'])
    def unfavourite(self, request, pk=None):
        event_to_unfav = self.get_object()
        event_to_unfav.favourited_users.remove(request.user)
        event_to_unfav.save()
        return Response({'status': 'unfavourited event'})

    @action(detail=True, methods=['post'])
    def register(self, request, pk=None):
        event_to_register = self.get_object()
        if event_to_register.registered_users.all().count() < event_to_register.event_max_capacity:
            event_to_register.registered_users.add(request.user)
            event_to_register.save()
            return Response({'status': 'registered event'})
        else:
            return Response('already in the limit of registered users',
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def unregister(self, request, pk=None):
        event_to_unregister = self.get_object()
        event_to_unregister.registered_users.remove(request.user)
        event_to_unregister.save()
        return Response({'status': 'unregistered event'})

    @action(detail=True, methods=['post'])
    def add_image(self, request, pk=None):
        event = self.get_object()

        #if images added, do the bindings
        if "event_media" not in request.data:
            return Response('no image uploaded',
                            status=status.HTTP_400_BAD_REQUEST)

        for image_data in request.data.getlist("event_media"):
            eventImage = EventImage.objects.create(event=event)
            eventImage.image.save(image_data.name, image_data)

        return Response({'status': 'image uploaded'})


    @action(detail=False, methods=['post'])
    def checkin_qrcode(self, request):
        qrcode = request.data.get("QRcode")
        qrdata = json.loads(qrcode)

        event_to_checkin = Event.objects.get(pk=qrdata["event_id"])
        #check that the request user is the host, such that he is allowed to check in people (TODO: let several people check-in others)
        if event_to_checkin.host.id is not request.user.id:
            return Response('you are not allowed to do check-ins for this event', status=status.HTTP_400_BAD_REQUEST)

        #check that this is a valid attendee
        atttendee_token = Token.objects.get(key=qrdata['attendee'])
        if atttendee_token is None:
            return Response('this is not a valid user', status=status.HTTP_400_BAD_REQUEST)

        attendee = User.objects.get(id=atttendee_token.user_id)
        if attendee is None:
            return Response('this is not a valid user', status=status.HTTP_400_BAD_REQUEST)

        #check that the attendee is a registered user
        if not event_to_checkin.registered_users.filter(pk=attendee.pk).exists():
            return Response('this user is not registered in the event', status=status.HTTP_400_BAD_REQUEST)

        event_to_checkin.attending_users.add(attendee)
        event_to_checkin.save()
        return Response({'status': 'user checked-in to event'})