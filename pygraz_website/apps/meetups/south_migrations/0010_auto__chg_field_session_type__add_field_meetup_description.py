from django.db import models
from south.db import db
from south.utils import datetime_utils as datetime
from south.v2 import SchemaMigration


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Changing field 'Session.type'
        db.alter_column(
            "meetups_session",
            "type_id",
            self.gf("django.db.models.fields.related.ForeignKey")(
                to=orm["meetups.SessionType"], null=True, on_delete=models.SET_NULL
            ),
        )
        # Adding field 'Meetup.description'
        db.add_column(
            "meetups_meetup",
            "description",
            self.gf("django.db.models.fields.TextField")(null=True, blank=True),
            keep_default=False,
        )

    def backwards(self, orm):
        # Changing field 'Session.type'
        db.alter_column(
            "meetups_session",
            "type_id",
            self.gf("django.db.models.fields.related.ForeignKey")(to=orm["meetups.SessionType"], null=True),
        )
        # Deleting field 'Meetup.description'
        db.delete_column("meetups_meetup", "description")

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
                "ordering": "(u'content_type__app_label', u'content_type__model', u'codename')",
                "unique_together": "((u'content_type', u'codename'),)",
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
                {"symmetrical": "False", "related_name": "u'user_set'", "blank": "True", "to": "orm['auth.Group']"},
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
                {
                    "symmetrical": "False",
                    "related_name": "u'user_set'",
                    "blank": "True",
                    "to": "orm['auth.Permission']",
                },
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
            "Meta": {"ordering": "('-start_date',)", "object_name": "Meetup"},
            "attendee_count": ("django.db.models.fields.IntegerField", [], {"null": "True", "blank": "True"}),
            "description": ("django.db.models.fields.TextField", [], {"null": "True", "blank": "True"}),
            "gplus_id": (
                "django.db.models.fields.CharField",
                [],
                {"max_length": "50", "null": "True", "blank": "True"},
            ),
            "id": ("django.db.models.fields.AutoField", [], {"primary_key": "True"}),
            "location": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {"to": "orm['meetups.Location']", "null": "True", "blank": "True"},
            ),
            "meetupcom_id": (
                "django.db.models.fields.CharField",
                [],
                {"max_length": "20", "null": "True", "blank": "True"},
            ),
            "notes": ("django.db.models.fields.TextField", [], {"null": "True", "blank": "True"}),
            "start_date": ("django.db.models.fields.DateTimeField", [], {}),
        },
        "meetups.rsvp": {
            "Meta": {"object_name": "RSVP"},
            "gplus_name": (
                "django.db.models.fields.CharField",
                [],
                {"max_length": "100", "null": "True", "blank": "True"},
            ),
            "gplus_uid": (
                "django.db.models.fields.CharField",
                [],
                {"max_length": "100", "null": "True", "blank": "True"},
            ),
            "id": ("django.db.models.fields.AutoField", [], {"primary_key": "True"}),
            "meetup": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {"related_name": "'rsvps'", "to": "orm['meetups.Meetup']"},
            ),
            "source": ("django.db.models.fields.CharField", [], {"max_length": "20", "null": "True", "blank": "True"}),
            "status": ("django.db.models.fields.CharField", [], {"max_length": "20", "null": "True", "blank": "True"}),
        },
        "meetups.session": {
            "Meta": {"object_name": "Session"},
            "abstract": ("django.db.models.fields.TextField", [], {}),
            "id": ("django.db.models.fields.AutoField", [], {"primary_key": "True"}),
            "meetup": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {"blank": "True", "related_name": "'sessions'", "null": "True", "to": "orm['meetups.Meetup']"},
            ),
            "notes": ("django.db.models.fields.TextField", [], {"null": "True", "blank": "True"}),
            "slides_url": (
                "django.db.models.fields.URLField",
                [],
                {"max_length": "200", "null": "True", "blank": "True"},
            ),
            "speaker": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {"to": "orm['auth.User']", "null": "True", "blank": "True"},
            ),
            "speaker_email": (
                "django.db.models.fields.EmailField",
                [],
                {"max_length": "75", "null": "True", "blank": "True"},
            ),
            "speaker_name": (
                "django.db.models.fields.CharField",
                [],
                {"max_length": "100", "null": "True", "blank": "True"},
            ),
            "title": ("django.db.models.fields.CharField", [], {"max_length": "255"}),
            "type": (
                "django.db.models.fields.related.ForeignKey",
                [],
                {"to": "orm['meetups.SessionType']", "null": "True", "on_delete": "models.SET_NULL", "blank": "True"},
            ),
        },
        "meetups.sessiontype": {
            "Meta": {"object_name": "SessionType"},
            "description": ("django.db.models.fields.TextField", [], {"null": "True", "blank": "True"}),
            "id": ("django.db.models.fields.AutoField", [], {"primary_key": "True"}),
            "name": ("django.db.models.fields.CharField", [], {"unique": "True", "max_length": "30"}),
        },
    }

    complete_apps = ["meetups"]
