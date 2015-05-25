import arrow
import datetime
import pytz
import re
import requests_mock

from django.utils import unittest, timezone
from django.core.exceptions import ValidationError
from django.core.management import call_command
from django.test import Client, TestCase
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


class MeetupCalendarViewTests(TestCase):
    def setUp(self):
        start = arrow.utcnow().replace(weeks=+1, hour=18)
        self.meetup = models.Meetup(start_date=start.datetime,
                                    meetupcom_id='test')
        self.meetup.save()

    def test_simple_calendar(self):
        resp = self.client.get('/meetups/ical/')
        self.assertEqual(200, resp.status_code)
        self.assertEqual('text/calendar', resp['Content-Type'])
        expected = """BEGIN:VCALENDAR\r
X-WR-CALNAME:PyGRAZ-Meetups\r
BEGIN:VEVENT\r
SUMMARY:PyGRAZ-Meetup am {date}\r
DTSTART;VALUE=DATE-TIME:{timestamp}\r
UID:example.com/meetups/1\r
DESCRIPTION:Details: https://example.com/meetups/{date}\r
END:VEVENT\r
END:VCALENDAR\r
""".format(
            date=arrow.get(self.meetup.start_date).format('YYYY-MM-DD'),
            timestamp=arrow.get(self.meetup.start_date).format('YYYYMMDDTHHmmss') + 'Z'
        )
        self.assertEqual(expected, resp.content)


class FetchRsvpsCommandTests(TestCase):
    def setUp(self):
        start = arrow.utcnow().replace(weeks=+1, hour=18)
        self.meetup = models.Meetup(start_date=start.datetime,
                                    meetupcom_id='test')
        self.meetup.save()
        models.Meetup(start_date=start.replace(months=+1).datetime).save()
        self.previous_rsvp = models.RSVP(
            meetup=self.meetup, status='coming',
            remote_username='test',
            remote_uid='test', source='meetupcom')
        self.previous_rsvp.save()

    def test_failure_should_keep_rsvps(self):
        with requests_mock.Mocker() as mock:
            mock.get(re.compile('api.meetup.com/2/rsvp'),
                     text='invalid_response')
            with self.assertRaises(Exception):
                call_command('fetch_rsvps')
            existing_rsvps = models.RSVP.objects.filter(
                meetup=self.meetup).all()
            self.assertEquals(len(list(existing_rsvps)), 1)

    def test_success(self):
        with requests_mock.Mocker() as mock:
            mock.get(re.compile('api.meetup.com/2/rsvp'), [
                {
                    'json': {
                        'meta': {
                            'count': 1,
                            'total_count': 2
                        },
                        'results': [
                            {
                                'response': 'no',
                                'member': {
                                    'name': 'new user',
                                    'member_id': '12345'
                                }
                            }
                        ]
                    }
                },
                {
                    'json': {
                        'meta': {
                            'count': 1,
                            'total_count': 2
                        },
                        'results': [
                            {
                                'response': 'yes',
                                'member': {
                                    'name': 'new user 2',
                                    'member_id': '12346'
                                }
                            }
                        ]
                    }
                }
            ])
            call_command('fetch_rsvps')
            rsvps = list(models.RSVP.objects.filter(meetup=self.meetup).all())
            self.assertEqual(2, len(rsvps))

            rsvp = rsvps[0]
            self.assertEqual('not_coming', rsvp.status)
            self.assertEqual('new user', rsvp.remote_username)
            self.assertEqual('12345', rsvp.remote_uid)
            self.assertEqual('meetupcom', rsvp.source)
            rsvp = rsvps[1]
            self.assertEqual('coming', rsvp.status)
            self.assertEqual('new user 2', rsvp.remote_username)
            self.assertEqual('12346', rsvp.remote_uid)
            self.assertEqual('meetupcom', rsvp.source)
