# -*- coding: utf-8 -*-
import datetime

from django.db import models
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding model 'Location'
        db.create_table(
            "meetups_location",
            (
                ("id", self.gf("django.db.models.fields.AutoField")(primary_key=True)),
                ("name", self.gf("django.db.models.fields.CharField")(max_length=200)),
                ("description", self.gf("django.db.models.fields.TextField")(null=True, blank=True)),
                ("website", self.gf("django.db.models.fields.URLField")(max_length=200, null=True, blank=True)),
                ("address", self.gf("django.db.models.fields.CharField")(max_length=255, null=True, blank=True)),
            ),
        )
        db.send_create_signal("meetups", ["Location"])

        # Adding model 'Meetup'
        db.create_table(
            "meetups_meetup",
            (
                ("id", self.gf("django.db.models.fields.AutoField")(primary_key=True)),
                ("start_date", self.gf("django.db.models.fields.DateTimeField")()),
                (
                    "location",
                    self.gf("django.db.models.fields.related.ForeignKey")(
                        to=orm["meetups.Location"], null=True, blank=True
                    ),
                ),
            ),
        )
        db.send_create_signal("meetups", ["Meetup"])

        # Adding model 'Session'
        db.create_table(
            "meetups_session",
            (
                ("id", self.gf("django.db.models.fields.AutoField")(primary_key=True)),
                ("title", self.gf("django.db.models.fields.CharField")(max_length=255)),
                ("abstract", self.gf("django.db.models.fields.TextField")()),
                (
                    "meetup",
                    self.gf("django.db.models.fields.related.ForeignKey")(
                        to=orm["meetups.Meetup"], null=True, blank=True
                    ),
                ),
                ("speaker_name", self.gf("django.db.models.fields.CharField")(max_length=100, null=True, blank=True)),
                (
                    "speaker",
                    self.gf("django.db.models.fields.related.ForeignKey")(to=orm["auth.User"], null=True, blank=True),
                ),
            ),
        )
        db.send_create_signal("meetups", ["Session"])

    def backwards(self, orm):
        # Deleting model 'Location'
        db.delete_table("meetups_location")

        # Deleting model 'Meetup'
        db.delete_table("meetups_meetup")

        # Deleting model 'Session'
        db.delete_table("meetups_session")

    models = {
        "auth.group": {
            "Meta": {"object_name": "Group"},
            "id": ("django.db.models.fields.AutoField", [], {"primary_key": "True"}),
            "name": ("django.db.models.fields.CharField", [], {"unique": "True", "max_length": "80"}),
            "permissions": (
                "django.db.models.fields.related.ManyToManyField",
                [],
                {"to": "orm['auth.Permission']", "symmetrical": "False", "blank": "True"},
            ),
        },
        "auth.permission": {
            "Meta": {
                "ordering": "('content_type__app_label', 'content_type__model', 'codename')",
                "unique_together": "(('content_type', 'codename'),)",
                "object_name": "Permission",
            },
            "codename": ("django.db.models.fields.CharField", [], {"max_length": "100"}),
            "content_type": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {"to": "orm['contenttypes.ContentType']"},
            ),
            "id": ("django.db.models.fields.AutoField", [], {"primary_key": "True"}),
            "name": ("django.db.models.fields.CharField", [], {"max_length": "50"}),
        },
        "auth.user": {
            "Meta": {"object_name": "User"},
            "date_joined": ("django.db.models.fields.DateTimeField", [], {"default": "datetime.datetime.now"}),
            "email": ("django.db.models.fields.EmailField", [], {"max_length": "75", "blank": "True"}),
            "first_name": ("django.db.models.fields.CharField", [], {"max_length": "30", "blank": "True"}),
            "groups": (
                "django.db.models.fields.related.ManyToManyField",
                [],
                {"to": "orm['auth.Group']", "symmetrical": "False", "blank": "True"},
            ),
            "id": ("django.db.models.fields.AutoField", [], {"primary_key": "True"}),
            "is_active": ("django.db.models.fields.BooleanField", [], {"default": "True"}),
            "is_staff": ("django.db.models.fields.BooleanField", [], {"default": "False"}),
            "is_superuser": ("django.db.models.fields.BooleanField", [], {"default": "False"}),
            "last_login": ("django.db.models.fields.DateTimeField", [], {"default": "datetime.datetime.now"}),
            "last_name": ("django.db.models.fields.CharField", [], {"max_length": "30", "blank": "True"}),
            "password": ("django.db.models.fields.CharField", [], {"max_length": "128"}),
            "user_permissions": (
                "django.db.models.fields.related.ManyToManyField",
                [],
                {"to": "orm['auth.Permission']", "symmetrical": "False", "blank": "True"},
            ),
            "username": ("django.db.models.fields.CharField", [], {"unique": "True", "max_length": "30"}),
        },
        "contenttypes.contenttype": {
            "Meta": {
                "ordering": "('name',)",
                "unique_together": "(('app_label', 'model'),)",
                "object_name": "ContentType",
                "db_table": "'django_content_type'",
            },
            "app_label": ("django.db.models.fields.CharField", [], {"max_length": "100"}),
            "id": ("django.db.models.fields.AutoField", [], {"primary_key": "True"}),
            "model": ("django.db.models.fields.CharField", [], {"max_length": "100"}),
            "name": ("django.db.models.fields.CharField", [], {"max_length": "100"}),
        },
        "meetups.location": {
            "Meta": {"object_name": "Location"},
            "address": (
                "django.db.models.fields.CharField",
                [],
                {"max_length": "255", "null": "True", "blank": "True"},
            ),
            "description": ("django.db.models.fields.TextField", [], {"null": "True", "blank": "True"}),
            "id": ("django.db.models.fields.AutoField", [], {"primary_key": "True"}),
            "name": ("django.db.models.fields.CharField", [], {"max_length": "200"}),
            "website": ("django.db.models.fields.URLField", [], {"max_length": "200", "null": "True", "blank": "True"}),
        },
        "meetups.meetup": {
            "Meta": {"object_name": "Meetup"},
            "id": ("django.db.models.fields.AutoField", [], {"primary_key": "True"}),
            "location": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {"to": "orm['meetups.Location']", "null": "True", "blank": "True"},
            ),
            "start_date": ("django.db.models.fields.DateTimeField", [], {}),
        },
        "meetups.session": {
            "Meta": {"object_name": "Session"},
            "abstract": ("django.db.models.fields.TextField", [], {}),
            "id": ("django.db.models.fields.AutoField", [], {"primary_key": "True"}),
            "meetup": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {"to": "orm['meetups.Meetup']", "null": "True", "blank": "True"},
            ),
            "speaker": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {"to": "orm['auth.User']", "null": "True", "blank": "True"},
            ),
            "speaker_name": (
                "django.db.models.fields.CharField",
                [],
                {"max_length": "100", "null": "True", "blank": "True"},
            ),
            "title": ("django.db.models.fields.CharField", [], {"max_length": "255"}),
        },
    }

    complete_apps = ["meetups"]
