from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import signals
import requests
import json
import jwt
import time
import pdb

from django.contrib.auth.models import User
from events.models import Event




@receiver(post_save, sender=User, dispatch_uid="user_creation_setup")
def post_user_creation_setup(sender, instance, created, **kwargs):
    if created:
        #create the user profile (TODO)
        #Profile.objects.create(user=instance)


        #create a JWT for pusher
        token = create_token_for_pusher()

        headers = {
            "Authorization": "Bearer " + token,
        }

        data = {
            "name" : instance.username,
            "id" : str(instance.pk)
        }

        #tell Pusher to create a new user
        request = requests.post('https://us1.pusherplatform.io/services/chatkit/v2/0fa52852-e026-4a78-b9fd-9ef562cc901c/users',
            headers=headers,
            json=data)

        #pdb.set_trace()



@receiver(post_save, sender=Event, dispatch_uid="event_creation_setup")
def post_event_creation_setup(sender, instance, created, **kwargs):
    if created:

        #create a JWT for pusher
        token = create_token_for_pusher()

        headers = {
            "Authorization": "Bearer " + token,
        }

        data = {
            "name" : instance.event_name,
            "user_ids" : [str(instance.host.pk)]
        }

        #tell Pusher to create a new user
        request = requests.post('https://us1.pusherplatform.io/services/chatkit/v2/0fa52852-e026-4a78-b9fd-9ef562cc901c/rooms',
            headers=headers,
            json=data)

        if request.status_code == 201:
            request_result = request.json()
            instance.room_id = request_result["id"]
            instance.save()

        #pdb.set_trace()


def create_token_for_pusher():
    key_secret = "ftQrAOm3k3zdq6YIOARDpq2HqGmq8hcmZp07arOxT44="
    curr_time = int(time.time())
    day = 86400
    exp_time = curr_time + day
    payload = {
    "instance": "0fa52852-e026-4a78-b9fd-9ef562cc901c",
    "iss": "api_keys/6da31832-1c47-48cc-ab3b-d02d54ed226c",
    "iat": curr_time,
    "exp": exp_time,
    "sub": "admin",
    "su": True
    }

    return jwt.encode(payload, key_secret, algorithm='HS256').decode('utf-8')


