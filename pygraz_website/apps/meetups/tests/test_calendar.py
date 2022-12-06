import arrow
from django.test import TestCase

from .. import models


class MeetupCalendarViewTests(TestCase):
    def setUp(self):
        start = arrow.utcnow().replace(month=1, day=2, hour=18)
        self.meetup = models.Meetup(start_date=start.datetime, meetupcom_id="test")
        self.meetup.save()

    def test_simple_calendar(self):
        resp = self.client.get("/meetups/ical/")
        self.assertEqual(200, resp.status_code)
        self.assertEqual("text/calendar", resp["Content-Type"])
        date = arrow.get(self.meetup.start_date).format("YYYY-MM-DD")
        timestamp = arrow.get(self.meetup.start_date).format("YYYYMMDDTHHmmss") + "Z"
        expected_content = (
            f"BEGIN:VCALENDAR\r\n"
            f"X-WR-CALNAME:PyGRAZ-Meetups\r\n"
            f"BEGIN:VEVENT\r\n"
            f"SUMMARY:PyGRAZ-Meetup am {date}\r\n"
            f"DTSTART:{timestamp}\r\n"
            f"UID:example.com/meetups/1\r\n"
            f"DESCRIPTION:Details: https://example.com/meetups/{date}/\r\n"
            f"END:VEVENT\r\n"
            f"END:VCALENDAR\r\n"
        ).encode()
        actual_content = resp.content
        self.assertEqual(expected_content, actual_content)
