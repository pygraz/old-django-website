import datetime
import pytz

from django.utils import unittest, timezone
from django.core.exceptions import ValidationError
from django.test import TestCase
from .. import models


class MeetupModelTests(TestCase):
    def test_required_fields(self):
        """
        Tests that only the start_date is required.
        """
        with self.assertRaises(ValidationError):
            models.Meetup().full_clean()
        models.Meetup(start_date=datetime.datetime.now().replace(tzinfo=pytz.UTC)).full_clean()

    def test_is_in_future(self):
        """
        Is_in_future should return true if the start_date of the meetup is in
        the future.
        """
        now = timezone.now()
        future_meetup = models.Meetup(start_date=now + datetime.timedelta(days=2))
        past_meetup = models.Meetup(start_date=now - datetime.timedelta(days=2))
        now_meetup = models.Meetup(start_date=now)
        self.assertTrue(future_meetup.is_in_future(now=now))
        self.assertFalse(past_meetup.is_in_future(now=now))
        self.assertFalse(now_meetup.is_in_future(now=now))

    def test_future_meetups_through_manager(self):
        """
        Tests that the manager returns future meetups as requested.
        """
        now = timezone.now()
        past_meetup = models.Meetup(start_date=now - datetime.timedelta(days=1)).save()
        now_meetup = models.Meetup(start_date=now).save()
        future_meetup_1 = models.Meetup(start_date=now + datetime.timedelta(days=1)).save()
        future_meetup_2 = models.Meetup(start_date=now + datetime.timedelta(days=2)).save()
        for m in models.Meetup.objects.get_future_meetups(now=now):
            self.assertTrue(m.is_in_future(now))

    def test_past_meetups_through_manager(self):
        """
        Tests that the manager returns future meetups as requested.
        """
        now = timezone.now()
        past_meetup = models.Meetup(start_date=now - datetime.timedelta(days=1)).save()
        now_meetup = models.Meetup(start_date=now).save()
        future_meetup_1 = models.Meetup(start_date=now + datetime.timedelta(days=1)).save()
        future_meetup_2 = models.Meetup(start_date=now + datetime.timedelta(days=2)).save()
        for m in models.Meetup.objects.get_past_meetups(now=now):
            self.assertFalse(m.is_in_future(now))

    def test_set_attendee_count(self):
        """
        It should be possible to set a number of attendees of a meetup outside
        of who responded to the RSVP.
        """
        models.Meetup(start_date=timezone.now(), attendee_count=10).full_clean()
        m = models.Meetup(start_date=timezone.now())
        m.attendee_count = 10

    def test_valid_attendee_count(self):
        """
        A valid number of attendees is a positive integer, 0 or None
        """
        t = timezone.now()
        meetup = models.Meetup(start_date=t)
        meetup.full_clean()
        meetup.attendee_count = None
        meetup.full_clean()
        meetup.attendee_count = 1
        meetup.full_clean()
        meetup.attendee_count = 10
        meetup.full_clean()
        meetup.attendee_count = 0
        meetup.full_clean()
        with self.assertRaises(ValidationError):
            meetup.attendee_count = -1
            meetup.full_clean()


class LocationModelTests(unittest.TestCase):
    def test_required_fields(self):
        """
        Only the name of the location is required.
        """
        with self.assertRaises(ValidationError):
            models.Location().full_clean()
        models.Location(name="Name").full_clean()


class SessionModelTests(unittest.TestCase):
    def test_required_fields(self):
        """
        Title and abstract are required.
        """
        with self.assertRaises(ValidationError):
            models.Session().full_clean()
        models.Session(title="title", abstract="abstract").full_clean()
