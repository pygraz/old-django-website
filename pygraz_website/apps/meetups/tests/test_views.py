from django.utils import timezone
from django.http import HttpResponseNotFound
from django.test import TestCase

from .. import models


class MeetupViewTests(TestCase):
    def setUp(self):
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
