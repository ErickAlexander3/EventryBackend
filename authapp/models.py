#from django.db import models
'''
# Create your models here.
from django.contrib.gis.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user   = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    #avatar = models.ImageField()
'''