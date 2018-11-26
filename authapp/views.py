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

    @action(detail=True, methods=['post'])
    def update_profile_pic(self, request, pk=None):
        user = self.get_object()

        #if images added, do the bindings
        if request.user.id != user.id:
            return Response("can't change someone else's profile pic",
                            status=status.HTTP_400_BAD_REQUEST)

        #if images added, do the bindings
        if "profile_pic" not in request.data:
            return Response('no image uploaded',
                            status=status.HTTP_400_BAD_REQUEST)

        pdb.set_trace()

        image_data = request.data.getlist("profile_pic")[0]
        user.user_profile.profile_pic = image_data
        user.user_profile.save()
        pdb.set_trace()
        return Response({'status': 'profile pic updated'})

    @action(detail=False, methods=['post'])
    def update_expo_token(self, request):
        if "expo_push_token" not in request.data:
            return Response('no token sent',
                            status=status.HTTP_400_BAD_REQUEST)

        user = self.request.user
        user.user_profile.expo_push_token = request.data["expo_push_token"]
        user.user_profile.save()
        return Response({'status': 'expo token updated'})

