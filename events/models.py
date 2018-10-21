from django.db import models

# Create your models here.
class Event(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    event_name = models.CharField(max_length=100, default='event')
    event_description = models.CharField(max_length=100, blank=True, default='')
    event_location = models.CharField(max_length=50)
    event_date = models.DateTimeField('date of event')
    event_participants = models.IntegerField(default=1)

    class Meta:
        ordering = ('creation_date',)