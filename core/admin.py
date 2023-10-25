from django.contrib import admin

from core.models import Location, Meetup, Session, SessionType

for model in [Location, Meetup, Session, SessionType]:
    admin.site.register(model)
