from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

import jwt
import time
import pdb

from allauth.account.signals import user_signed_up


from django.db.models import signals


@receiver(post_save, sender=User)
def post_user_creation_setup(sender, instance, created, **kwargs):
    if created:
        #create the user profile (TODO)
        #Profile.objects.create(user=instance)


        #create a JWT for pusher
        key_secret = "ftQrAOm3k3zdq6YIOARDpq2HqGmq8hcmZp07arOxT44="
        curr_time = int(time.time())
        day = 86400
        exp_time = curr_time + day - 1000
        payload = {
          "instance": "0fa52852-e026-4a78-b9fd-9ef562cc901c",
          "iss": "api_keys/6da31832-1c47-48cc-ab3b-d02d54ed226c",
          "iat": curr_time,
          "exp": exp_time,
          "sub": "EventryServer",
          "su": True
        }

        token = jwt.encode(payload, key_secret, algorithm='HS256')

        #tell Pusher to create a new user
        #pdb.set_trace()

