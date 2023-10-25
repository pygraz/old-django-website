import random
from datetime import date, datetime, timedelta, timezone

from django.contrib.auth.models import User
from django.db import transaction

from core.models import Location, Meetup, Session, SessionType

DEMO_ADMIN_USERNAMES = ["admin"]
DEMO_COMMON_USERNAMES = ["alice", "bob", "clara", "dean"]
DEMO_LOCATION_NAMES = ["Spektral", "Gösserbräu"]
DEMO_SESSION_TYPE_NAMES = ["Coding Dojo", "Lightning Talk", "Talk"]
_DEMO_PACKAGES = ["cheese", "eggs", "ham", "parrot", "spam"]
_DEMO_TITLE_FORMATS = [
    "Everything you need ot know about %(package)s",
    "Understanding %(package)s",
    "Working with %(package)s",
    "%(package)s - an introduction",
]
_DAYS_BETWEEN_SESSION = 30


def purge_demo():
    User.objects.filter(username__in=DEMO_ADMIN_USERNAMES + DEMO_COMMON_USERNAMES).delete()
    for model in [Location, Session, SessionType, Meetup]:
        model.objects.all().delete()


def build_demo(session_count: int = 20):
    randomizer = random.Random(0)
    for admin_username in DEMO_ADMIN_USERNAMES:
        build_user_if_not_exists(admin_username, True)
    for common_username in DEMO_COMMON_USERNAMES:
        build_user_if_not_exists(common_username)
    for location_name in DEMO_LOCATION_NAMES:
        Location.objects.update_or_create(name=location_name)
    for session_type_name in DEMO_SESSION_TYPE_NAMES:
        SessionType.objects.update_or_create(name=session_type_name)
    meetup_date = utc_now() + timedelta(days=11 - _DAYS_BETWEEN_SESSION * (session_count - 2))
    locations = list(Location.objects.order_by("id"))
    session_types = list(SessionType.objects.order_by("id"))
    for _ in range(session_count):
        location = randomizer.choice(locations)
        meetup, _ = Meetup.objects.update_or_create(start_date=meetup_date, defaults={"location": location})
        session_type = randomizer.choice(session_types)
        package_name = randomizer.choice(_DEMO_PACKAGES)
        title_format = randomizer.choice(_DEMO_TITLE_FORMATS)
        title = title_format % {"package": package_name}
        Session.objects.update_or_create(title=title, defaults={"type": session_type})
        # TODO Session.objects.create(meetup=meetup, title=title, type=session_type)
        meetup_date = meetup_date + timedelta(days=_DAYS_BETWEEN_SESSION)


def build_user_if_not_exists(username: str, is_superuser: bool = False):
    with transaction.atomic():
        user = User.objects.select_for_update().filter(username=username)
        if user is None:
            User.objects.create_user(username=username, is_staff=is_superuser, is_superuser=is_superuser)


def utc_now() -> datetime:
    return datetime.utcnow().replace(tzinfo=timezone.utc)
