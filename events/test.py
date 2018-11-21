from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import timedelta
from django.utils import timezone

from events.models import Event


class EventTestCase(TestCase):
    def setUp(self):
        #set event with basic required data to avoid assertion issues
        event = Event.objects.create(event_location='here', event_start_time=timezone.now() + timedelta(minutes = 30), event_end_time= timezone.now() +timedelta(minutes = 60) )


    def test_cant_define_creation_date_manually(self):
        """Date of creation of event should be defined by the database and can't be set manually"""
        wrong_date = timezone.now() - timedelta(minutes = 30)
        event = Event.objects.create(creation_date = wrong_date, event_location='here', event_start_time=timezone.now() + timedelta(minutes = 30), event_end_time= timezone.now() +timedelta(minutes = 60) )
        event.full_clean()
        event.save()
        self.assertNotEqual(event.creation_date, wrong_date)

    
    def test_cant_create_event_with_negative_participants(self):
        """We should only have a non-negative number of participants"""
        event = Event.objects.get(id = 1)

        with self.assertRaises(ValidationError):
            event.event_participants = -1
            event.full_clean()
            event.save()


    def test_cant_create_event_with_negative_price(self):
        """We should only have a non-negative price"""
        event = Event.objects.get(id = 1)

        with self.assertRaises(ValidationError):
            event.event_price = -1
            event.full_clean()
            event.save()

    def test_cant_create_event_with_start_time_before_now(self):
        """We should only have a non-negative price"""
        event = Event.objects.get(id = 1)

        with self.assertRaises(ValidationError):
            wrong_date = timezone.now() - timedelta(minutes = 30)
            event.event_start_time = wrong_date
            event.full_clean()
            event.save()

    def test_cant_create_event_with_end_time_before_now(self):
        """We should only have a non-negative price"""
        event = Event.objects.get(id = 1)

        with self.assertRaises(ValidationError):
            wrong_date = timezone.now() - timedelta(minutes = 30)
            event.event_end_time = wrong_date
            event.full_clean()
            event.save()

    def test_cant_create_event_with_end_time_before_start_time(self):
        """We should only have a non-negative price"""
        event = Event.objects.get(id = 1)

        with self.assertRaises(ValidationError):
            wrong_start_time = timezone.now() + timedelta(minutes = 60)
            wrong_end_time = timezone.now() + timedelta(minutes = 30)
            event.event_start_time = wrong_start_time
            event.event_end_time = wrong_end_time
            event.full_clean()
            event.save()