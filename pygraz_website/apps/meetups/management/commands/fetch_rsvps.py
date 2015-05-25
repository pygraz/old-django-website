import logging
import requests

from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction

from ... import models


LOG = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Fetches RSVP responses from services like Google+ for future events"

    def _fetch_from_meetupcom(self, meetup):
        rsvps = []
        meetupcom_id = meetup.meetupcom_id
        seen = 0
        while True:
            resp = requests.get('https://api.meetup.com/2/rsvps', params={
                'key': settings.MEETUPCOM_API_KEY,
                'event_id': meetupcom_id,
                'sign': True,
                'offset': seen,
                'format': 'json',
            })
            result = resp.json()
            seen += result['meta']['count']
            for rsvp in result['results']:
                # meetup.com has no "maybe" status
                status = 'coming' if rsvp['response'] == 'yes' else 'not_coming'
                rsvps.append(models.RSVP(
                    status=status,
                    remote_username=rsvp['member']['name'],
                    remote_uid=rsvp['member']['member_id'],
                    source='meetupcom',
                    meetup=meetup
                ))
            if seen >= result['meta']['total_count']:
                break

        with transaction.atomic():
            models.RSVP.objects.filter(meetup=meetup, source='meetupcom').delete()
            for rsvp in rsvps:
                rsvp.save()

    def handle(self, *args, **options):
        for meetup in models.Meetup.objects.get_future_meetups():
            if meetup.meetupcom_id:
                self._fetch_from_meetupcom(meetup)
