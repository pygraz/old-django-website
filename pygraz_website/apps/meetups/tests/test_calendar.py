import arrow
from django.test import TestCase

from .. import models


class MeetupCalendarViewTests(TestCase):
    def setUp(self):
        start = arrow.utcnow().replace(weeks=+1, hour=18)
        self.meetup = models.Meetup(start_date=start.datetime, meetupcom_id="test")
        self.meetup.save()

    def test_simple_calendar(self):
        resp = self.client.get("/meetups/ical/")
        self.assertEqual(200, resp.status_code)
        self.assertEqual("text/calendar", resp["Content-Type"])
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
            date=arrow.get(self.meetup.start_date).format("YYYY-MM-DD"),
            timestamp=arrow.get(self.meetup.start_date).format("YYYYMMDDTHHmmss") + "Z",
        )
        self.assertEqual(expected, resp.content)
