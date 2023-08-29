from django.contrib.auth import models as auth_models
from django.contrib.sites.models import Site
from django.core import validators
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from pygraz_website.apps.accounts import contents

RSVP_STATUS_CHOICES = (
    ("not_coming", _("Not coming")),
    ("coming", _("Coming")),
    ("maybe", _("Maybe")),
)


class MeetupManager(models.Manager):
    def get_past_meetups(self, now=None):
        """
        Adds a filter for meetups that started in the past.
        """
        if now is None:
            now = timezone.now()
        return self.get_queryset().filter(start_date__lte=now)

    def get_future_meetups(self, now=None):
        if now is None:
            now = timezone.now()
        return self.get_queryset().filter(start_date__gt=now)


class SessionManager(models.Manager):
    def get_proposals(self):
        """
        Adds a filter for sessions that are not assigned to a meetup yet.
        """
        return self.get_queryset().filter(meetup__isnull=True)


class Location(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    map_image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("location")
        verbose_name_plural = _("locations")


class Meetup(models.Model):
    start_date = models.DateTimeField()
    location = models.ForeignKey(Location, blank=True, null=True, on_delete=models.CASCADE)
    meetupcom_id = models.CharField(blank=True, null=True, max_length=20)
    gplus_id = models.CharField(blank=True, null=True, max_length=50)
    description = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    attendee_count = models.IntegerField(
        null=True,
        blank=True,
        validators=[
            validators.MinValueValidator(0),
        ],
    )

    objects = MeetupManager()

    def __str__(self):
        return str(self.start_date)

    def get_absolute_url(self):
        return reverse(
            "view-meetup",
            kwargs={
                "year": f"{self.start_date.year:0>4d}",
                "month": f"{self.start_date.month:0>2}",
                "day": f"{self.start_date.day:0>2d}",
            },
        )

    def get_permalink(self):
        return "http://{}{}".format(
            Site.objects.get_current().domain,
            reverse("meetup-permalink", kwargs={"pk": self.pk}),
        )

    def get_meetupcom_url(self):
        return f"http://www.meetup.com/PyGRAZ/events/{self.meetupcom_id}"

    def is_in_future(self, now=None):
        if now is None:
            now = timezone.now()
        return self.start_date > now

    class Meta:
        verbose_name = "Meetup"
        verbose_name_plural = "Meetups"
        ordering = ("-start_date",)


class Session(models.Model):
    title = models.CharField("Titel", max_length=255)
    abstract = models.TextField("Kurzbeschreibung")
    meetup = models.ForeignKey(
        Meetup,
        verbose_name="Meetup",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="sessions",
    )
    speaker_name = models.CharField("Vortragender", max_length=100, blank=True, null=True)
    speaker_email = models.EmailField("E-Mail-Adresse", blank=True, null=True)
    speaker = models.ForeignKey(
        auth_models.User,
        verbose_name="Vortragender",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    slides_url = models.URLField("Folien-URL", blank=True, null=True)
    notes = models.TextField("Notizen", blank=True, null=True)
    type = models.ForeignKey(
        "SessionType",
        verbose_name="Vortragsart",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    objects = SessionManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("view-session", kwargs={"pk": self.pk})

    def get_permalink(self):
        return f"http://{Site.objects.get_current()}{self.get_absolute_url()}"

    def get_speaker_name(self):
        if self.speaker:
            firstname = self.speaker.first_name
            lastname = self.speaker.last_name
            if firstname is not None and lastname is not None:
                return f"{firstname} {lastname}"
            if firstname is not None:
                return firstname
            return self.speaker.username
        return self.speaker_name

    class Meta:
        verbose_name = "Session"
        verbose_name_plural = "Sessions"


class SessionType(models.Model):
    name = models.CharField("Name", max_length=30, unique=True)
    description = models.TextField("Beschreibung", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Session type"
        verbose_name_plural = "Session types"


class SessionContentProxy(contents.BaseProxy):
    model_class = Session
    label = "Meine Sessions"

    def get_queryset(self):
        return Session.objects.filter(speaker=self.request.user)


contents.register(SessionContentProxy)


class RSVP(models.Model):
    """
    A RSVP object represents the status of attendence of a person at a meetup.
    The source of this information in the current implementation is Meetup.com
    and not linked to a local user account.

    The status can be either coming, not coming, maybe or unknown (represented
    by a null value).
    """

    status = models.CharField(_("Status"), choices=RSVP_STATUS_CHOICES, null=True, blank=True, max_length=20)
    remote_username = models.CharField(_("Username"), null=True, blank=True, max_length=100)
    remote_uid = models.CharField(_("User ID"), null=True, blank=True, max_length=100)
    meetup = models.ForeignKey(
        "Meetup",
        null=False,
        verbose_name=_("Meetup"),
        on_delete=models.CASCADE,
        related_name="rsvps",
    )
    source = models.CharField(max_length=20, blank=True, null=True)

    @property
    def name(self):
        return self.remote_username

    @property
    def url(self):
        return f"http://www.meetup.com/members/{self.remote_uid}/"

    class Meta:
        verbose_name = _("RSVP")
        verbose_name_plural = _("RSVPs")
