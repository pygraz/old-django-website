# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("meetups", "0002_rsvp_refactoring"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rsvp",
            name="remote_uid",
            field=models.CharField(max_length=100, null=True, verbose_name="User ID", blank=True),
        ),
        migrations.AlterField(
            model_name="rsvp",
            name="remote_username",
            field=models.CharField(max_length=100, null=True, verbose_name="Username", blank=True),
        ),
        migrations.AlterField(
            model_name="session",
            name="speaker_email",
            field=models.EmailField(max_length=254, null=True, verbose_name="E-Mail-Adresse", blank=True),
        ),
    ]
