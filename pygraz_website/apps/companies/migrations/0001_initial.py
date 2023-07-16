# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Company",
            fields=[
                ("id", models.AutoField(verbose_name="ID", serialize=False, auto_created=True, primary_key=True)),
                ("name", models.CharField(max_length=100, verbose_name="name")),
                ("website", models.URLField(verbose_name="website")),
                ("contact_email", models.EmailField(max_length=75, verbose_name="contact e-mail", blank=True)),
                ("description", models.TextField(verbose_name="description", blank=True)),
                ("address_line", models.CharField(max_length=255, verbose_name="address line")),
                ("postal_code", models.CharField(max_length=10, verbose_name="postal code")),
                ("city", models.CharField(max_length=50, verbose_name="city")),
                ("country", models.CharField(max_length=3, verbose_name="country", choices=[(b"AT", "Austria")])),
                ("approved", models.BooleanField(default=False, verbose_name="approved")),
                ("pub_date", models.DateTimeField(auto_now_add=True, verbose_name="Published at")),
                (
                    "editors",
                    models.ManyToManyField(
                        related_name="companies", null=True, to=settings.AUTH_USER_MODEL, blank=True
                    ),
                ),
            ],
            options={
                "ordering": ("name",),
                "verbose_name": "company",
                "verbose_name_plural": "companies",
            },
            bases=(models.Model,),
        ),
    ]
