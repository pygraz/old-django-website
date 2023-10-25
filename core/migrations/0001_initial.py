import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Location",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200)),
                ("description", models.TextField(blank=True, default="")),
                ("website", models.URLField(blank=True, default="")),
                ("address", models.CharField(blank=True, default="", max_length=255)),
                ("map_image", models.ImageField(blank=True, default=None, null=True, upload_to="")),
            ],
            options={
                "verbose_name": "location",
                "verbose_name_plural": "locations",
            },
        ),
        migrations.CreateModel(
            name="Meetup",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("start_date", models.DateField()),
                ("meetupcom_id", models.CharField(blank=True, default="", max_length=20)),
                ("description", models.TextField(blank=True, default="")),
                ("notes", models.TextField(blank=True, default="")),
                (
                    "attendee_count",
                    models.IntegerField(
                        blank=True, null=True, validators=[django.core.validators.MinValueValidator(0)]
                    ),
                ),
                (
                    "location",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="core.location",
                    ),
                ),
            ],
            options={
                "verbose_name": "Meetup",
                "verbose_name_plural": "Meetups",
                "ordering": ("-start_date",),
            },
        ),
        migrations.CreateModel(
            name="SessionType",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=30, unique=True, verbose_name="Name")),
                ("description", models.TextField(blank=True, default="", verbose_name="Beschreibung")),
            ],
            options={
                "verbose_name": "Session type",
                "verbose_name_plural": "Session types",
            },
        ),
        migrations.CreateModel(
            name="Session",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255, verbose_name="Titel")),
                ("abstract", models.TextField(verbose_name="Kurzbeschreibung")),
                ("speaker_name", models.CharField(blank=True, default="", max_length=100, verbose_name="Vortragender")),
                (
                    "speaker_email",
                    models.EmailField(blank=True, default="", max_length=254, verbose_name="E-Mail-Adresse"),
                ),
                ("slides_url", models.URLField(blank=True, default="", verbose_name="Folien-URL")),
                ("notes", models.TextField(blank=True, default="", verbose_name="Notizen")),
                (
                    "meetup",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sessions",
                        to="core.meetup",
                        verbose_name="Meetup",
                    ),
                ),
                (
                    "speaker",
                    models.ForeignKey(
                        blank=True,
                        default="",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Vortragender",
                    ),
                ),
                (
                    "type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="core.sessiontype", verbose_name="Vortragsart"
                    ),
                ),
            ],
            options={
                "verbose_name": "Session",
                "verbose_name_plural": "Sessions",
            },
        ),
    ]
