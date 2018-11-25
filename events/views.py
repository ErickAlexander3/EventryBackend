import json
from events.serializers import EventSerializer
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User
from events.models import Event

import pdb

class EventViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)
        '''
    def create(self, request, *args, **kwargs):
        pdb.set_trace()
        return super(EventViewSet, self).create(request, *args, **kwargs)
        '''
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

    @action(detail=False)
    def registered(self, request):
        registered_events = Event.objects.filter(registered_users__id=request.user.pk)
        serializer = self.get_serializer(registered_events, many=True)
        return Response(serializer.data)

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