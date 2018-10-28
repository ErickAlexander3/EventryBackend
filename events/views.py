from events.models import Event
from events.serializers import EventSerializer
from rest_framework import viewsets

class EventViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer