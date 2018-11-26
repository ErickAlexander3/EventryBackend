#from django.db import models
from django.contrib.gis.db import models
from django.core.validators import MinValueValidator
from django.contrib.postgres.fields import ArrayField
from enum import Enum

import os
from uuid import uuid4

def path_and_rename(instance, filename):
    upload_to = 'event_pics'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


# Create your models here.
class Event(models.Model):
    EVENT_TYPE = (
        ("FO", "Food"),
        ("NT", "Networking"),
        ("PT", "Party"),
        ("SP", "Sports"),
        ("AC", "Academics"),
        ("MU", "Music"),
        ("MS", "Miscellaneous"),
    )

    host = models.ForeignKey('auth.User', related_name='events_hosting', on_delete=models.CASCADE, default=1)
    registered_users = models.ManyToManyField('auth.User', related_name='events_registered')
    attending_users = models.ManyToManyField('auth.User', related_name='events_attended')
    favourited_users = models.ManyToManyField('auth.User', related_name='events_favourited')
    creation_date = models.DateTimeField(auto_now_add=True)
    event_name = models.CharField(max_length=100, default='event')
    event_description = models.CharField(max_length=100, blank=True, default='New event')
    event_address = models.CharField(max_length=50, null=True, blank=True)
    event_point_location = models.PointField(null=True)
    event_max_capacity = models.PositiveIntegerField(default=100) #NOTE: the redundant validator was just added for compatibility with SQLite
    event_type = ArrayField(
        models.CharField(choices=EVENT_TYPE, max_length=2, blank=True, default="MS"),
        default=list,
        null=True
    )
    event_start_time = models.DateTimeField('start date and time', null=True)
    event_end_time = models.DateTimeField('start date and time', null=True)
    event_price = models.DecimalField(max_digits=7, decimal_places=2, default='0.00', validators=[MinValueValidator(0.0)])
    room_id = models.CharField(max_length=150, null=True)


    class Meta:
        ordering = ('-creation_date',)


class EventImage(models.Model):
        event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="event_media")
        image = models.ImageField(upload_to=path_and_rename)



    

