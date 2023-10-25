from typing import Optional

from django.contrib.auth.models import User
from django.core import validators
from django.db import models
from django.db.models import QuerySet
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class Location(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")
    website = models.URLField(blank=True, default="")
    address = models.CharField(default="", blank=True, max_length=255)
    map_image = models.ImageField(default=None, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("location")
        verbose_name_plural = _("locations")


class MeetupManager(models.Manager):
    def past_meetups(self) -> QuerySet["Meetup"]:
        return self.filter(start_date__lt=now())

    def next_meetup(self) -> Optional["Meetup"]:
        return self.filter(start_date__gte=now()).first()


class Meetup(models.Model):
    objects = MeetupManager()

    start_date = models.DateField()
    location = models.ForeignKey(Location, blank=True, default=None, null=True, on_delete=models.CASCADE)
    meetupcom_id = models.CharField(
        blank=True, default="", max_length=20, help_text=_("ID part of URL from meetup.com")
    )
    description = models.TextField(blank=True, default="")
    notes = models.TextField(blank=True, default="")
    attendee_count = models.IntegerField(
        null=True,
        blank=True,
        validators=[
            validators.MinValueValidator(0),
        ],
    )

    @property
    def meetup_url(self):
        return f"https://www.meetup.com/PyGRAZ/events/{self.meetupcom_id}"

    def __str__(self):
        return str(self.start_date)

    class Meta:
        verbose_name = "Meetup"
        verbose_name_plural = "Meetups"
        ordering = ("-start_date",)


class Session(models.Model):
    title = models.CharField("Titel", max_length=255)
    abstract = models.TextField("Kurzbeschreibung")
    meetup: Meetup = models.ForeignKey(
        Meetup,
        blank=True,
        default=None,
        null=True,
        on_delete=models.CASCADE,
        related_name="sessions",
        verbose_name="Meetup",
    )
    speaker_name = models.CharField("Vortragender", blank=True, default="", max_length=100)
    speaker_email = models.EmailField("E-Mail-Adresse", blank=True, default="")
    speaker: User = models.ForeignKey(
        User,
        verbose_name="Vortragender",
        blank=True,
        default="",
        null=True,
        on_delete=models.CASCADE,
    )
    slides_url = models.URLField("Folien-URL", blank=True, default="")
    notes = models.TextField("Notizen", blank=True, default="")
    type = models.ForeignKey(
        "SessionType",
        verbose_name="Vortragsart",
        on_delete=models.PROTECT,
    )

    def __str__(self):
        return self.title

    @property
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
    description = models.TextField("Beschreibung", blank=True, default="")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Session type"
        verbose_name_plural = "Session types"
