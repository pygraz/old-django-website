# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("companies", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="company",
            name="contact_email",
            field=models.EmailField(max_length=254, verbose_name="contact e-mail", blank=True),
        ),
    ]
