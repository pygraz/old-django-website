from django.contrib import admin
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from . import models


class AssignedMeetupFilter(admin.SimpleListFilter):
    """
    Filters sessions that are assigned to a meetup.
    """

    parameter_name = "assigned"
    title = "hat Meetup"

    def lookups(self, request, model_admin):
        return (
            ("assigned", _("Yes")),
            ("unassigned", _("No")),
        )

    def queryset(self, request, queryset):
        val = self.value()
        if not val:
            return queryset
        return queryset.filter(meetup__isnull=(val != "assigned"))


class SessionWithSlidesFilter(admin.SimpleListFilter):
    """
    Filters session that contain a link to slides.
    """

    parameter_name = "has_slides"
    title = "hat Folien"

    def lookups(self, request, model_admin):
        return (
            ("yes", _("Yes")),
            ("no", _("No")),
        )

    def queryset(self, request, queryset):
        val = self.value()
        if not val:
            return queryset
        if val == "yes":
            return queryset.exclude(Q(slides_url__isnull=True) | Q(slides_url=""))
        else:
            return queryset.filter(Q(slides_url__isnull=True) | Q(slides_url=""))


class SessionBySpeakerType(admin.SimpleListFilter):
    """
    Filters sessions by the type of speaker they have set: anonymous or
    registered.
    """

    parameter_name = "speakertype"
    title = _("speaker type")

    def lookups(self, request, model_admin):
        return (
            ("anon", _("Anonymous")),
            ("reg", _("Registered")),
        )

    def queryset(self, request, queryset):
        val = self.value()
        if not val:
            return queryset
        return queryset.filter(speaker__isnull=(val == "anon"))


class MeetupComAvailable(admin.SimpleListFilter):
    """
    Filters meetups that have a meetupcom_id assigned.
    """

    parameter_name = "meetupcom_available"
    title = _("meetup.com available")

    def lookups(self, request, model_admin):
        return (("yes", _("Yes")), ("no", _("No")))

    def queryset(self, request, queryset):
        val = self.value()
        if not val:
            return queryset
        if val == "no":
            return queryset.filter(Q(meetupcom_id="") | Q(meetupcom_id__isnull=True))
        else:
            return queryset.exclude(Q(meetupcom_id="") | Q(meetupcom_id__isnull=True))


class RSVPAdmin(admin.ModelAdmin):
    list_display = ["meetup", "remote_username", "status", "source"]
    list_filter = ["meetup"]


class SessionTypeAdmin(admin.ModelAdmin):
    pass


admin.site.register(
    models.Meetup,
    list_display=["start_date", "location", "attendee_count"],
    list_filter=[
        MeetupComAvailable,
    ],
)
admin.site.register(
    models.Session,
    list_display=["title", "meetup", "type", "speaker", "speaker_name"],
    list_filter=[
        "type",
        AssignedMeetupFilter,
        SessionBySpeakerType,
        SessionWithSlidesFilter,
    ],
)
admin.site.register(
    models.Location,
    list_display=["name"],
)

admin.site.register(models.RSVP, RSVPAdmin)
admin.site.register(models.SessionType, SessionTypeAdmin)
