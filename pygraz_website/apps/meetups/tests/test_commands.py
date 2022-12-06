import re

import arrow
import requests_mock
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from .. import models


class FetchRsvpsCommandTests(TestCase):
    def setUp(self):

        future_year = timezone.now().year + 2
        start = arrow.utcnow().replace(year=future_year, month=1, day=2, hour=18)
        self.meetup = models.Meetup(start_date=start.datetime, meetupcom_id="test")
        self.meetup.save()
        models.Meetup(start_date=start.replace(year=future_year, month=2).datetime).save()
        self.previous_rsvp = models.RSVP(
            meetup=self.meetup, status="coming", remote_username="test", remote_uid="test", source="meetupcom"
        )
        self.previous_rsvp.save()

    def test_failure_should_keep_rsvps(self):
        with requests_mock.Mocker() as mock:
            mock.get(re.compile("api.meetup.com/2/rsvp"), text="invalid_response")
            with self.assertRaises(Exception):
                call_command("fetch_rsvps")
            existing_rsvps = models.RSVP.objects.filter(meetup=self.meetup).all()
            self.assertEqual(len(list(existing_rsvps)), 1)

    def test_success(self):
        with requests_mock.Mocker() as mock:
            mock.get(
                re.compile("api.meetup.com/2/rsvp"),
                [
                    {
                        "json": {
                            "meta": {"count": 1, "total_count": 2},
                            "results": [{"response": "no", "member": {"name": "new user", "member_id": "12345"}}],
                        }
                    },
                    {
                        "json": {
                            "meta": {"count": 1, "total_count": 2},
                            "results": [{"response": "yes", "member": {"name": "new user 2", "member_id": "12346"}}],
                        }
                    },
                ],
            )
            call_command("fetch_rsvps")
            rsvps = list(models.RSVP.objects.filter(meetup=self.meetup).all())
            self.assertEqual(2, len(rsvps))

            rsvp = rsvps[0]
            self.assertEqual("not_coming", rsvp.status)
            self.assertEqual("new user", rsvp.remote_username)
            self.assertEqual("12345", rsvp.remote_uid)
            self.assertEqual("meetupcom", rsvp.source)
            rsvp = rsvps[1]
            self.assertEqual("coming", rsvp.status)
            self.assertEqual("new user 2", rsvp.remote_username)
            self.assertEqual("12346", rsvp.remote_uid)
            self.assertEqual("meetupcom", rsvp.source)
