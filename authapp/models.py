#from django.db import models

# Create your models here.
from django.contrib.gis.db import models
from django.contrib.auth.models import User

import os
from uuid import uuid4

def path_and_rename(instance, filename):
    upload_to = 'profile_pics'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    bio = models.CharField(max_length=1000, default="I'm a cool user for using Eventry... and I won't fail CPEN 321!")
    profile_pic = models.ImageField(upload_to=path_and_rename)
