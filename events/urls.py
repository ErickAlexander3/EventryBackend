from events.views import EventViewSet, api_root
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path

event_list = EventViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
event_detail = EventViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = format_suffix_patterns([
    path('', event_list, name='event-list'),
    path('<int:pk>', event_detail, name='event-detail'),
])