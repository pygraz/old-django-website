# -*- coding: utf-8 -*-
import datetime

from django.db import models
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding model 'Company'
        db.create_table(
            "companies_company",
            (
                ("id", self.gf("django.db.models.fields.AutoField")(primary_key=True)),
                ("name", self.gf("django.db.models.fields.CharField")(max_length=100)),
                ("website", self.gf("django.db.models.fields.URLField")(max_length=200)),
                ("contact_email", self.gf("django.db.models.fields.EmailField")(max_length=75, blank=True)),
                ("description", self.gf("django.db.models.fields.TextField")(blank=True)),
                ("address_line", self.gf("django.db.models.fields.CharField")(max_length=255)),
                ("postal_code", self.gf("django.db.models.fields.CharField")(max_length=10)),
                ("city", self.gf("django.db.models.fields.CharField")(max_length=50)),
                ("country", self.gf("django.db.models.fields.CharField")(max_length=3)),
                ("approved", self.gf("django.db.models.fields.BooleanField")(default=False)),
            ),
        )
        db.send_create_signal("companies", ["Company"])

        # Adding M2M table for field editors on 'Company'
        db.create_table(
            "companies_company_editors",
            (
                ("id", models.AutoField(verbose_name="ID", primary_key=True, auto_created=True)),
                ("company", models.ForeignKey(orm["companies.company"], null=False)),
                ("user", models.ForeignKey(orm["auth.user"], null=False)),
            ),
        )
        db.create_unique("companies_company_editors", ["company_id", "user_id"])

    def backwards(self, orm):
        # Deleting model 'Company'
        db.delete_table("companies_company")

        # Removing M2M table for field editors on 'Company'
        db.delete_table("companies_company_editors")

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
        "companies.company": {
            "Meta": {"object_name": "Company"},
            "address_line": ("django.db.models.fields.CharField", [], {"max_length": "255"}),
            "approved": ("django.db.models.fields.BooleanField", [], {"default": "False"}),
            "city": ("django.db.models.fields.CharField", [], {"max_length": "50"}),
            "contact_email": ("django.db.models.fields.EmailField", [], {"max_length": "75", "blank": "True"}),
            "country": ("django.db.models.fields.CharField", [], {"max_length": "3"}),
            "description": ("django.db.models.fields.TextField", [], {"blank": "True"}),
            "editors": (
                "django.db.models.fields.related.ManyToManyField",
                [],
                {
                    "blank": "True",
                    "related_name": "'companies'",
                    "null": "True",
                    "symmetrical": "False",
                    "to": "orm['auth.User']",
                },
            ),
            "id": ("django.db.models.fields.AutoField", [], {"primary_key": "True"}),
            "name": ("django.db.models.fields.CharField", [], {"max_length": "100"}),
            "postal_code": ("django.db.models.fields.CharField", [], {"max_length": "10"}),
            "website": ("django.db.models.fields.URLField", [], {"max_length": "200"}),
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
    }

    complete_apps = ["companies"]
