import json
import subprocess
import logging

from django.core.management.base import BaseCommand

from ... import models


LOG = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Fetches RSVP responses from services like Google+ for future events"

    def handle(self, *args, **options):
        for meetup in models.Meetup.objects.get_future_meetups():
            rsvps = meetup.rsvps.filter(source='gplus')
            if meetup.gplus_id:
                LOG.debug("Fetching Google+ data for meetup ", meetup)
                # Fetch the data
                data = subprocess.check_output(['casperjs', 'tools/fetch_rsvps.js', meetup.gplus_id])
                rsvp_map = {}
                for rsvp in rsvps:
                    rsvp_map[rsvp.gplus_uid] = rsvp
                rsvp_set = set(rsvp_map.keys())
                new_rsvps = {}
                fetched_rsvps = json.loads(data)
                for obj in fetched_rsvps['coming']:
                    obj['status'] = 'coming'
                    new_rsvps[obj['id']] = obj
                for obj in fetched_rsvps['maybe']:
                    obj['status'] = 'maybe'
                    new_rsvps[obj['id']] = obj
                for obj in fetched_rsvps['not_coming']:
                    obj['status'] = 'not_coming'
                    new_rsvps[obj['id']] = obj
                new_rsvp_ids = set(new_rsvps.keys())

                ids_to_remove = rsvp_set - new_rsvp_ids
                LOG.debug("IDs to remove: ", ids_to_remove)

                models.RSVP.objects.filter(source='gplus',
                    meetup=meetup, gplus_uid__in=ids_to_remove).delete()

                new_ids_to_add = new_rsvp_ids - rsvp_set
                LOG.debug("IDs to add:", new_ids_to_add)

                for id_ in new_ids_to_add:
                    models.RSVP(
                        source='gplus',
                        gplus_uid=id_, 
                        status=new_rsvps[id_]['status'],
                        gplus_name=new_rsvps[id_]['name'],
                        meetup=meetup).save()
