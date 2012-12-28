import datetime
import pytz

from django.utils import unittest, timezone
from django.core.exceptions import ValidationError
from django.test import Client
from django.db import IntegrityError
from django.http import HttpResponseNotFound

from . import models


class MeetupModelTests(unittest.TestCase):
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


class MeetupViewTests(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.now = timezone.now()
        self.past_meetup = models.Meetup(start_date=self.now - timezone.timedelta(days=2))
        self.past_meetup.save()
        self.future_meetup = models.Meetup(start_date=self.now + timezone.timedelta(days=2))
        self.future_meetup.save()

    def tearDown(self):
        self.future_meetup.delete()
        self.past_meetup.delete()

    def test_view_not_existing(self):
        """
        Tests that a request for a not-existing meetup results in a 404 page.
        """
        self.assertTrue(isinstance(self.client.get('/meetups/123/'), HttpResponseNotFound))

    def test_view_existing(self):
        """
        Tests that a meetup can be accessed by its URL.
        """
        self.assertEquals(200, self.client.get('/meetups/{0}/'.format(self.past_meetup.pk)).status_code)

    def test_upcoming_on_frontpage(self):
        """
        Tests that the next meetup is displayed on the frontpage.
        """
        resp = self.client.get('/')
        self.assertEquals(200, resp.status_code)
        self.assertEquals(self.future_meetup, resp.context['next_meetup'])
