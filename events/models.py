#from django.db import models
from django.contrib.gis.db import models
from django.core.validators import MinValueValidator
from django.contrib.postgres.fields import ArrayField
from enum import Enum


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
        default=list
    )
    event_start_time = models.DateTimeField('start date and time', null=True)
    event_end_time = models.DateTimeField('start date and time', null=True)
    event_price = models.DecimalField(max_digits=7, decimal_places=2, default='0.00', validators=[MinValueValidator(0.0)])
    event_qrenabled = models.BooleanField(default=False)
    event_pic = models.ImageField(upload_to='event_pics/', default='event_picts/None/no-img.jpg')



    class Meta:
        ordering = ('creation_date',)

    

