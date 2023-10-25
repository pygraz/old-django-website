from django.core.management import CommandError
from django.core.management.base import BaseCommand
from django.db.models import ProtectedError

from demo.demo import build_demo, purge_demo


class Command(BaseCommand):
    help = "Add demo data to database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--purge", "-P", action="store_true", help="Purge all existing data before creating new one"
        )

    def handle(self, *_args, **options):
        has_to_be_purged = bool(options["purge"])

        try:
            if has_to_be_purged:
                purge_demo()
            build_demo()
        except ProtectedError as error:
            raise CommandError(f"Cannot create demo: {error}") from error
        else:
            self.stdout.write(self.style.SUCCESS("Successfully created demo"))
