from django.shortcuts import render
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView
from rest_framework.decorators import action
from rest_framework.response import Response

from django.contrib.auth.models import User
from rest_framework import status, viewsets
from .serializers import UserSerializer

import pdb

class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter

class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


def privacy_policy(request):
    return render(request, 'privacy_policy.html')


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list`, `retrieve`,

    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False)
    def attending_event(self, request):
        if 'event_id' not in request.query_params:
            return Response('not a valid event_id', status=status.HTTP_400_BAD_REQUEST)

        users_attending_event = self.queryset.filter(events_attended__id=request.query_params.get("event_id"))

        #pdb.set_trace()
        serializer = self.get_serializer(users_attending_event, many=True)
        return Response(serializer.data)
