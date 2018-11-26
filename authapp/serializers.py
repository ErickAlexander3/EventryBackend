'''
from events.models import Event
from drf_extra_fields.geo_fields import PointField
from rest_framework.fields import ListField
'''

from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

from django.contrib.auth.models import User

class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', '')
        }


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile_pic = serializers.ImageField(source='user_profile.profile_pic')
    number_of_attending_events = serializers.IntegerField(source='events_attended.count', read_only=True)
    number_of_hosting_events = serializers.IntegerField(source='events_hosting.count', read_only=True)
    bio = serializers.ReadOnlyField(source='user_profile.bio')
    expo_push_token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'profile_pic',
            'bio',
            'number_of_attending_events',
            'number_of_hosting_events',
            'expo_push_token'
        )

    def get_expo_push_token(self, obj):
        if self.context["request"].user.id == obj.id:
            return obj.user_profile.expo_push_token
        else:
            return None