# Generated by Django 4.0.8 on 2022-11-05 15:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("meetups", "0003_field_lengths"),
    ]

    operations = [
        migrations.AlterField(
            model_name="meetup",
            name="location",
            field=models.ForeignKey(
                blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to="meetups.location"
            ),
        ),
        migrations.AlterField(
            model_name="rsvp",
            name="meetup",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="rsvps",
                to="meetups.meetup",
                verbose_name="Meetup",
            ),
        ),
        migrations.AlterField(
            model_name="rsvp",
            name="status",
            field=models.CharField(
                blank=True,
                choices=[("not_coming", "Not coming"), ("coming", "Coming"), ("maybe", "Maybe")],
                max_length=20,
                null=True,
                verbose_name="Status",
            ),
        ),
        migrations.AlterField(
            model_name="session",
            name="abstract",
            field=models.TextField(verbose_name="Kurzbeschreibung"),
        ),
        migrations.AlterField(
            model_name="session",
            name="meetup",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="sessions",
                to="meetups.meetup",
                verbose_name="Meetup",
            ),
        ),
        migrations.AlterField(
            model_name="session",
            name="notes",
            field=models.TextField(blank=True, null=True, verbose_name="Notizen"),
        ),
        migrations.AlterField(
            model_name="session",
            name="slides_url",
            field=models.URLField(blank=True, null=True, verbose_name="Folien-URL"),
        ),
        migrations.AlterField(
            model_name="session",
            name="speaker",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
                verbose_name="Vortragender",
            ),
        ),
        migrations.AlterField(
            model_name="session",
            name="speaker_name",
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name="Vortragender"),
        ),
        migrations.AlterField(
            model_name="session",
            name="title",
            field=models.CharField(max_length=255, verbose_name="Titel"),
        ),
        migrations.AlterField(
            model_name="session",
            name="type",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="meetups.sessiontype",
                verbose_name="Vortragsart",
            ),
        ),
        migrations.AlterField(
            model_name="sessiontype",
            name="description",
            field=models.TextField(blank=True, null=True, verbose_name="Beschreibung"),
        ),
        migrations.AlterField(
            model_name="sessiontype",
            name="name",
            field=models.CharField(max_length=30, unique=True, verbose_name="Name"),
        ),
    ]
